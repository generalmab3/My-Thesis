@echo off
rem Build slides.pdf with XeLaTeX (run from this folder or double-click)
cd /d "%~dp0"
where xelatex >nul 2>nul
if errorlevel 1 (
  echo [ERROR] xelatex not found on PATH.
  echo Please install MiKTeX ^(https://miktex.org/^) or TeX Live and try again.
  pause
  exit /b 1
)
echo === XeLaTeX pass 1/2 ===
xelatex -interaction=nonstopmode slides.tex
if errorlevel 1 (
  echo [ERROR] First pass failed. See slides.log for details.
  pause
  exit /b 1
)
echo === XeLaTeX pass 2/2 ===
xelatex -interaction=nonstopmode slides.tex
if errorlevel 1 (
  echo [ERROR] Second pass failed. See slides.log for details.
  pause
  exit /b 1
)
echo.
echo Done: slides.pdf
pause
