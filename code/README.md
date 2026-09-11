# کد پیاده‌سازی پایان‌نامه

پیاده‌سازی مدل زمان‌پیوسته شبکه عصبی آگاه از فیزیک (PINN) برای معادله
برگرز یک‌بعدی، شامل مسئله مستقیم (یافتن جواب) و مسئله معکوس (کشف
پارامترها)، بر اساس مقاله رئیسی و همکاران (2019).

## نصب پیش‌نیازها

```bash
pip install -r requirements.txt
```

## اجرا

اجرای کامل (مستقیم + معکوس بدون نویز + معکوس با نویز یک درصد):

```bash
python pinn_burgers.py --mode all
```

فقط مسئله مستقیم:

```bash
python pinn_burgers.py --mode forward --adam-iters 4000 --lbfgs-maxfun 2500
```

فقط مسئله معکوس:

```bash
python pinn_burgers.py --mode inverse --adam-iters 4000 --lbfgs-maxfun 2000
```

## خروجی‌ها

همه خروجی‌ها در پوشه `../figs/` ذخیره می‌شوند:

- `forward_metrics.json` و `inverse_metrics_*.json`: معیارهای عددی
- `burgers_snapshots.pdf`: مقایسه جواب دقیق و شبکه در سه لحظه زمانی
- `loss_history.pdf`: نمودار همگرایی آموزش
- `error_heatmap.pdf`: نقشه خطای مطلق در دامنه زمانی-مکانی
- `forward_points.pdf` و `inverse_points.pdf`: نقاط آموزشی
