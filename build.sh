#!/bin/bash
# ساخت پایان‌نامه با زی‌لاتک (دو بار اجرا برای فهرست‌ها و ارجاع‌ها)
set -e
cd "$(dirname "$0")"
xelatex -interaction=nonstopmode thesis.tex
xelatex -interaction=nonstopmode thesis.tex
echo "Done: thesis.pdf"
