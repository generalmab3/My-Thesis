#!/bin/bash
# ساخت اسلایدها با زی‌لاتک
set -e
cd "$(dirname "$0")"
xelatex -interaction=nonstopmode slides.tex
xelatex -interaction=nonstopmode slides.tex
echo "Done: slides.pdf"
