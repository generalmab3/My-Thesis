#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics-Informed Neural Network (PINN) for the 1D Burgers equation.

Reproduction (for B.Sc. thesis) of the continuous-time results of:
  Raissi, Perdikaris, Karniadakis, "Physics-informed neural networks...",
  J. Comput. Phys. 378 (2019) 686-707.  (Appendix A.1 and B.1)

Two modes:
  forward : data-driven solution of Burgers (learn u(t,x) from IC/BC + PDE residual)
  inverse : data-driven discovery of Burgers (learn lambda1, lambda2 from scattered data)

Burgers equation:  u_t + lambda1 * u * u_x - lambda2 * u_xx = 0
  x in [-1, 1], t in [0, 1], lambda1 = 1.0, lambda2 = 0.01/pi (forward)
  u(0, x) = -sin(pi*x), u(t, -1) = u(t, 1) = 0

Reference solution: Fourier spectral in space (N=512, 2/3 de-aliasing) + RK4 in time.

Requirements: jax[cpu], numpy, scipy, matplotlib
Output: metrics JSON + figures written to ../figs/
"""
import argparse
import json
import os
import time

import numpy as np

import jax
from jax import grad, jit, vmap
from jax.tree_util import tree_map
from jax.flatten_util import ravel_pytree
import jax.numpy as jnp
from jax import random

try:
    jax.config.update("jax_enable_x64", True)
except Exception:  # very old jax
    from jax import config as _cfg
    _cfg.update("jax_enable_x64", True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(os.path.dirname(HERE), "figs")
os.makedirs(FIGDIR, exist_ok=True)

PI = float(np.pi)
NU = 0.01 / PI  # viscosity used in the paper


# ----------------------------------------------------------------------------
# Reference spectral solver (independent of the neural network)
# ----------------------------------------------------------------------------
def burgers_reference(nx=1024, dt=0.001, t_out=None, nu=NU):
    """Solve Burgers with Fourier spectral + ETDRK4 (Kassam & Trefethen 2005).

    The diffusion term is treated exactly in Fourier space, so the scheme
    stays stable for the stiff thin shock layer. Returns t, x, U[nt, nx].
    """
    L = 2.0
    x = np.linspace(-1.0, 1.0, nx, endpoint=False)
    k = 2.0 * PI * np.fft.fftfreq(nx, d=L / nx)
    dealias = (np.abs(k) < (nx // 3) * (2.0 * PI / L)).astype(float)

    # ETDRK4 coefficients via contour integral (M points on unit circle)
    M = 32
    r = np.exp(1j * PI * (np.arange(1, M + 1) - 0.5) / M)
    Lv = -nu * k ** 2
    LR = dt * Lv[:, None] + r[None, :]
    E = np.exp(dt * Lv)
    E2 = np.exp(dt * Lv / 2.0)
    Q = dt * np.real(np.mean((np.exp(LR / 2.0) - 1.0) / LR, axis=1))
    f1 = dt * np.real(np.mean(
        (-4.0 - LR + np.exp(LR) * (4.0 - 3.0 * LR + LR ** 2)) / LR ** 3, axis=1))
    f2 = dt * np.real(np.mean(
        2.0 * (2.0 + LR + np.exp(LR) * (-2.0 + LR)) / LR ** 3, axis=1))
    f3 = dt * np.real(np.mean(
        (-4.0 - 3.0 * LR - LR ** 2 + np.exp(LR) * (4.0 - LR)) / LR ** 3, axis=1))

    def nlin(uu):
        uh = np.fft.fft(uu)
        ux = np.real(np.fft.ifft(1j * k * uh))
        return np.fft.fft(-uu * ux) * dealias

    u = -np.sin(PI * x)
    v = np.fft.fft(u)
    if t_out is None:
        t_out = np.linspace(0, 1.0, 101)
    U = [u.copy()]
    t = 0.0
    for target in t_out[1:]:
        nsteps = int(round((target - t) / dt))
        for _ in range(nsteps):
            Nv = nlin(np.real(np.fft.ifft(v)))
            a = E2 * v + Q * Nv
            Na = nlin(np.real(np.fft.ifft(a)))
            b = E2 * v + Q * Na
            Nb = nlin(np.real(np.fft.ifft(b)))
            c = E2 * a + Q * (2.0 * Nb - Nv)
            Nc = nlin(np.real(np.fft.ifft(c)))
            v = E * v + f1 * Nv + f2 * (Na + Nb) + f3 * Nc
            t += dt
        U.append(np.real(np.fft.ifft(v)))
    U = np.array(U)
    assert np.all(np.isfinite(U)), "reference solver diverged!"
    return t_out, x, U


# ----------------------------------------------------------------------------
# MLP + derivatives (automatic differentiation)
# ----------------------------------------------------------------------------
def init_mlp(key, layers):
    keys = random.split(key, len(layers) - 1)
    params = []
    for kk, (din, dout) in zip(keys, zip(layers[:-1], layers[1:])):
        W = random.normal(kk, (din, dout)) * np.sqrt(2.0 / (din + dout))
        b = jnp.zeros((dout,))
        params.append((W, b))
    return params


def u_point(params, t, x):
    h = jnp.stack([t, x])
    for W, b in params[:-1]:
        h = jnp.tanh(jnp.dot(h, W) + b)
    W, b = params[-1]
    return jnp.dot(h, W)[0] + b[0]


_u_t = grad(u_point, argnums=1)
_u_x = grad(u_point, argnums=2)
_u_xx = grad(grad(u_point, argnums=2), argnums=2)

u_pred = jit(vmap(u_point, in_axes=(None, 0, 0)))
u_t_pred = jit(vmap(_u_t, in_axes=(None, 0, 0)))
u_x_pred = jit(vmap(_u_x, in_axes=(None, 0, 0)))
u_xx_pred = jit(vmap(_u_xx, in_axes=(None, 0, 0)))


# ----------------------------------------------------------------------------
# Manual Adam (no extra dependencies, works with any jax version)
# ----------------------------------------------------------------------------
def adam(loss_grad_fn, params, iters, lr=1e-3, log_every=500, tag="adam"):
    m = tree_map(jnp.zeros_like, params)
    v = tree_map(jnp.zeros_like, params)
    b1, b2, eps = 0.9, 0.999, 1e-8
    hist = []
    for it in range(1, iters + 1):
        loss, g = loss_grad_fn(params)
        m = tree_map(lambda mm, gg: b1 * mm + (1 - b1) * gg, m, g)
        v = tree_map(lambda vv, gg: b2 * vv + (1 - b2) * (gg ** 2), v, g)
        mh = tree_map(lambda mm: mm / (1 - b1 ** it), m)
        vh = tree_map(lambda vv: vv / (1 - b2 ** it), v)
        params = tree_map(lambda p, mm, vv: p - lr * mm / (jnp.sqrt(vv) + eps),
                          params, mh, vh)
        hist.append(float(loss))
        if it % log_every == 0 or it == 1:
            print(f"[{tag}] iter {it:5d}/{iters}  loss = {float(loss):.6e}", flush=True)
    return params, hist


def lbfgs(loss_fn, grad_fn, params, maxfun=2000):
    from scipy.optimize import minimize
    x0, unravel = ravel_pytree(params)
    x0 = np.asarray(x0, dtype=np.float64)

    def fun(x):
        return float(loss_fn(unravel(jnp.asarray(x))))

    def jac(x):
        g = grad_fn(unravel(jnp.asarray(x)))
        flat, _ = ravel_pytree(g)
        return np.asarray(flat, dtype=np.float64)

    state = {"n": 0, "hist": []}

    def cb(x):
        state["n"] += 1
        if state["n"] % 200 == 0:
            print(f"[lbfgs] eval {state['n']}  loss = {fun(x):.6e}", flush=True)

    t0 = time.time()
    res = minimize(fun, x0, jac=jac, method="L-BFGS-B",
                   callback=cb,
                   options={"maxfun": maxfun, "maxiter": maxfun,
                            "ftol": 1e-12, "gtol": 1e-10})
    print(f"[lbfgs] done: {res.message}  fun={res.fun:.6e}  "
          f"nit={res.nit} nfev={res.nfev}  time={time.time()-t0:.1f}s", flush=True)
    return unravel(jnp.asarray(res.x, dtype=jnp.float64)), float(res.fun)


# ----------------------------------------------------------------------------
# Forward problem
# ----------------------------------------------------------------------------
def run_forward(adam_iters=6000, lbfgs_maxfun=6000, seed=0):
    rng = np.random.RandomState(seed)
    print("== forward: solving reference ==", flush=True)
    t_g, x_g, Uref = burgers_reference()
    print(f"   reference grid: t={t_g.shape}, x={x_g.shape}, "
          f"|u|max at t=1: {np.abs(Uref[-1]).max():.4f}", flush=True)

    # Training data: Nu points on initial + boundary
    Nu0, Nub = 100, 100
    x0 = rng.uniform(-1, 1, Nu0)
    t0 = np.zeros_like(x0)
    u0 = -np.sin(PI * x0)
    tb = rng.uniform(0, 1, Nub)
    xb = rng.choice([-1.0, 1.0], size=Nub)
    ub = np.zeros_like(tb)
    t_u = np.concatenate([t0, tb])
    x_u = np.concatenate([x0, xb])
    u_u = np.concatenate([u0, ub])

    # Collocation points: half uniform + half clustered around the shock (x=0),
    # where the solution develops a steep front for t > ~0.3.
    Nf1, Nf2 = 5000, 5000
    t_f1 = rng.uniform(0, 1, Nf1)
    x_f1 = rng.uniform(-1, 1, Nf1)
    t_f2 = rng.uniform(0, 1, Nf2)
    x_f2 = np.clip(rng.normal(0.0, 0.2, Nf2), -1.0, 1.0)
    t_f = np.concatenate([t_f1, t_f2])
    x_f = np.concatenate([x_f1, x_f2])
    Nf = Nf1 + Nf2

    t_u_ = jnp.asarray(t_u); x_u_ = jnp.asarray(x_u); u_u_ = jnp.asarray(u_u)
    t_f_ = jnp.asarray(t_f); x_f_ = jnp.asarray(x_f)

    layers = [2, 50, 50, 50, 50, 1]
    params = init_mlp(random.PRNGKey(seed), layers)
    npar = sum(w.size + b.size for w, b in params)
    print(f"== forward: network {layers}  params={npar}  "
          f"Nu={len(t_u)} Nf={Nf} ==", flush=True)

    @jit
    def loss_fn(p):
        mse_u = jnp.mean((u_pred(p, t_u_, x_u_) - u_u_) ** 2)
        uu = u_pred(p, t_f_, x_f_)
        f = (u_t_pred(p, t_f_, x_f_) + uu * u_x_pred(p, t_f_, x_f_)
             - NU * u_xx_pred(p, t_f_, x_f_))
        mse_f = jnp.mean(f ** 2)
        return mse_u + mse_f

    @jit
    def grad_fn(p):
        return grad(loss_fn)(p)

    def loss_grad(p):
        return loss_fn(p), grad_fn(p)

    print(f"[forward] initial loss = {float(loss_fn(params)):.6e}", flush=True)
    t_start = time.time()
    params, hist_adam = adam(loss_grad, params, adam_iters, lr=1e-3,
                             log_every=500, tag="forward/adam")
    params, loss_lbfgs = lbfgs(loss_fn, grad_fn, params, maxfun=lbfgs_maxfun)
    print(f"[forward] total time = {time.time()-t_start:.1f}s", flush=True)
    mse_u_fin = float(jnp.mean((u_pred(params, t_u_, x_u_) - u_u_) ** 2))
    _uu = u_pred(params, t_f_, x_f_)
    _ff = (u_t_pred(params, t_f_, x_f_) + _uu * u_x_pred(params, t_f_, x_f_)
           - NU * u_xx_pred(params, t_f_, x_f_))
    mse_f_fin = float(jnp.mean(_ff ** 2))
    print(f"[forward] final MSE_u = {mse_u_fin:.6e}, MSE_f = {mse_f_fin:.6e}",
          flush=True)

    # Evaluate on the full reference grid
    TT, XX = np.meshgrid(t_g, x_g, indexing="ij")
    Up = np.asarray(u_pred(params, jnp.asarray(TT.ravel()),
                           jnp.asarray(XX.ravel()))).reshape(TT.shape)
    err = np.linalg.norm(Up - Uref) / np.linalg.norm(Uref)
    print(f"[forward] relative L2 error = {err:.6e}", flush=True)

    metrics = {
        "mode": "forward",
        "layers": layers, "n_params": int(npar),
        "Nu": int(len(t_u)), "Nf": int(Nf),
        "adam_iters": adam_iters, "lbfgs_maxfun": lbfgs_maxfun,
        "loss_adam_final": hist_adam[-1], "loss_lbfgs_final": loss_lbfgs,
        "mse_u_final": mse_u_fin, "mse_f_final": mse_f_fin,
        "rel_l2": float(err), "seed": seed,
        "nu": NU,
    }
    with open(os.path.join(FIGDIR, "forward_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
    np.savez(os.path.join(FIGDIR, "forward_data.npz"),
             t=t_g, x=x_g, Uref=Uref, Upred=Up,
             hist_adam=np.array(hist_adam),
             t_u=t_u, x_u=x_u)

    # --- figures ---
    plt.rcParams.update({"font.size": 11})
    # 1) snapshots
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.2), sharey=True)
    for ax, tc in zip(axes, [0.25, 0.5, 0.75]):
        i = int(np.argmin(np.abs(t_g - tc)))
        ax.plot(x_g, Uref[i], "k-", lw=1.6, label="Exact")
        ax.plot(x_g, Up[i], "r--", lw=1.3, label="PINN")
        ax.set_title(f"t = {t_g[i]:.2f}")
        ax.set_xlabel("x")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("u(t, x)")
    axes[0].legend(frameon=True)
    fig.suptitle("Burgers equation: exact vs PINN (forward problem)")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "burgers_snapshots.pdf"))
    plt.close(fig)

    # 2) loss history (raw curve + running minimum, as Adam is spiky)
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    hist_adam = np.asarray(hist_adam)
    runmin = np.minimum.accumulate(hist_adam)
    ax.semilogy(hist_adam, color="lightsteelblue", lw=0.8, label="Adam (raw)")
    ax.semilogy(runmin, "b-", lw=1.4, label="Adam (running min)")
    ax.axhline(loss_lbfgs, color="r", ls="--", lw=1.2, label="L-BFGS (final)")
    ax.set_xlabel("Adam iteration")
    ax.set_ylabel("Loss (MSE_u + MSE_f)")
    ax.set_title("Training loss history (forward problem)")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "loss_history.pdf"))
    plt.close(fig)

    # 3) error heatmap
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    im = ax.imshow(np.abs(Up - Uref), origin="lower", aspect="auto",
                   extent=[x_g[0], x_g[-1], t_g[0], t_g[-1]], cmap="hot")
    ax.set_xlabel("x")
    ax.set_ylabel("t")
    ax.set_title("Absolute error |u_exact - u_pinn| (forward problem)")
    fig.colorbar(im, ax=ax, label="|error|")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "error_heatmap.pdf"))
    plt.close(fig)

    # 4) training points
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.scatter(t_f[::5], x_f[::5], s=3, c="lightsteelblue", label="Collocation (subset)")
    ax.scatter(t_u, x_u, s=14, c="red", marker="x", label="IC/BC data")
    ax.set_xlabel("t")
    ax.set_ylabel("x")
    ax.set_title("Training points (forward problem)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "forward_points.pdf"))
    plt.close(fig)
    print("[forward] figures saved.", flush=True)
    return metrics


# ----------------------------------------------------------------------------
# Inverse problem (discovery of lambda1, lambda2)
# ----------------------------------------------------------------------------
def run_inverse(n_data=5000, noise=0.0, adam_iters=6000, lbfgs_maxfun=6000,
               seed=1):
    rng = np.random.RandomState(seed)
    print(f"== inverse: n={n_data}, noise={noise} ==", flush=True)
    t_g, x_g, Uref = burgers_reference()
    # scattered observations: half uniform + half clustered around the shock,
    # where the u_xx term (hence lambda2) actually matters.
    n1, n2 = n_data // 2, n_data - n_data // 2
    ti = np.concatenate([rng.uniform(0, 1, n1), rng.uniform(0, 1, n2)])
    xi = np.concatenate([rng.uniform(-1, 1, n1),
                         np.clip(rng.normal(0.0, 0.2, n2), -1.0, 1.0)])
    ii = np.clip((ti * (len(t_g) - 1)).astype(int), 0, len(t_g) - 1)
    jj = np.clip(((xi + 1) / 2 * (len(x_g))).astype(int), 0, len(x_g) - 1)
    ui = Uref[ii, jj].copy()
    if noise > 0:
        ui = ui + noise * np.std(ui) * rng.randn(n_data)

    t_d = jnp.asarray(ti); x_d = jnp.asarray(xi); u_d = jnp.asarray(ui)

    layers = [2, 30, 30, 30, 30, 30, 1]
    params = init_mlp(random.PRNGKey(seed), layers)
    lam = jnp.array([0.0, 0.0])  # lambda1, lambda2 to be identified
    npar = sum(w.size + b.size for w, b in params) + 2
    print(f"== inverse: network {layers} params={npar} ==", flush=True)

    @jit
    def loss_fn(pl):
        p, l = pl
        mse_u = jnp.mean((u_pred(p, t_d, x_d) - u_d) ** 2)
        uu = u_pred(p, t_d, x_d)
        f = (u_t_pred(p, t_d, x_d) + l[0] * uu * u_x_pred(p, t_d, x_d)
             - l[1] * u_xx_pred(p, t_d, x_d))
        return mse_u + jnp.mean(f ** 2)

    @jit
    def grad_fn(pl):
        return grad(loss_fn)(pl)

    def loss_grad(pl):
        return loss_fn(pl), grad_fn(pl)

    print(f"[inverse] initial loss = {float(loss_fn((params, lam))):.6e}", flush=True)
    t_start = time.time()
    (params, lam), hist_adam = adam(loss_grad, (params, lam), adam_iters,
                                    lr=1e-3, log_every=500, tag="inverse/adam")
    (params, lam), loss_lbfgs = lbfgs(loss_fn, grad_fn, (params, lam),
                                      maxfun=lbfgs_maxfun)
    print(f"[inverse] total time = {time.time()-t_start:.1f}s", flush=True)

    lam = np.asarray(lam, dtype=float)
    true = np.array([1.0, NU])
    pct = 100.0 * np.abs(lam - true) / np.abs(true)
    print(f"[inverse] identified lambda = {lam}, true = {true}", flush=True)
    print(f"[inverse] percentage errors = {pct}%", flush=True)

    metrics = {
        "mode": "inverse", "layers": layers, "n_params": int(npar),
        "n_data": n_data, "noise": noise,
        "adam_iters": adam_iters, "lbfgs_maxfun": lbfgs_maxfun,
        "loss_adam_final": float(hist_adam[-1]),
        "loss_lbfgs_final": float(loss_lbfgs),
        "lambda_identified": [float(lam[0]), float(lam[1])],
        "lambda_true": [1.0, NU],
        "pct_error": [float(pct[0]), float(pct[1])],
        "seed": seed,
    }
    tag = f"inverse_metrics_noise{int(100*noise)}.json"
    with open(os.path.join(FIGDIR, tag), "w") as f:
        json.dump(metrics, f, indent=2)

    # scatter figure (only for the clean case to keep the thesis light)
    if noise == 0.0:
        fig, ax = plt.subplots(figsize=(6.2, 3.8))
        sc = ax.scatter(ti, xi, s=6, c=ui, cmap="seismic", vmin=-1, vmax=1)
        ax.set_xlabel("t")
        ax.set_ylabel("x")
        ax.set_title(f"Scattered training data (inverse problem, N={n_data})")
        fig.colorbar(sc, ax=ax, label="u(t, x)")
        fig.tight_layout()
        fig.savefig(os.path.join(FIGDIR, "inverse_points.pdf"))
        plt.close(fig)
    return metrics


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["forward", "inverse", "all"],
                    default="all")
    ap.add_argument("--adam-iters", type=int, default=6000)
    ap.add_argument("--lbfgs-maxfun", type=int, default=6000)
    args = ap.parse_args()

    all_metrics = {}
    if args.mode in ("forward", "all"):
        all_metrics["forward"] = run_forward(
            adam_iters=args.adam_iters, lbfgs_maxfun=args.lbfgs_maxfun)
    if args.mode in ("inverse", "all"):
        all_metrics["inverse_clean"] = run_inverse(
            noise=0.0, adam_iters=args.adam_iters,
            lbfgs_maxfun=args.lbfgs_maxfun)
        all_metrics["inverse_noisy"] = run_inverse(
            noise=0.01, adam_iters=args.adam_iters,
            lbfgs_maxfun=args.lbfgs_maxfun, seed=2)
    with open(os.path.join(FIGDIR, "metrics_all.json"), "w") as f:
        json.dump(all_metrics, f, indent=2, default=str)
    print("ALL DONE. metrics:", json.dumps(all_metrics, indent=2, default=str),
          flush=True)


if __name__ == "__main__":
    main()
