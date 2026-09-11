all: thesis.pdf

thesis.pdf: thesis.tex front/*.tex chapters/*.tex back/*.tex code/pinn_burgers.py figs/*
	xelatex -interaction=nonstopmode thesis.tex
	xelatex -interaction=nonstopmode thesis.tex

clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.synctex.gz *.bbl *.blg

.PHONY: all clean
