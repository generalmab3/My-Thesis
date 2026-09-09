@echo off
rem Build both thesis.pdf and slides.pdf (double-click from repo root)
cd /d "%~dp0"
where xelatex >nul 2>nul
if errorlevel 1 (
  echo [ERROR] xelatex not found on PATH.
  echo Please install MiKTeX ^(https://miktex.org/^) or TeX Live and try again.
  pause
  exit /b 1
)
echo ########## Building thesis ##########
cd thesis
xelatex -interaction=nonstopmode thesis.tex >nul
xelatex -interaction=nonstopmode thesis.tex
if errorlevel 1 (
  echo [ERROR] thesis build failed. See thesis\thesis.log for details.
  cd ..
  pause
  exit /b 1
)
cd ..
echo.
echo ########## Building slides ##########
cd defense
xelatex -interaction=nonstopmode slides.tex >nul
xelatex -interaction=nonstopmode slides.tex
if errorlevel 1 (
  echo [ERROR] slides build failed. See defense\slides.log for details.
  cd ..
  pause
  exit /b 1
)
cd ..
echo.
echo Done: thesis\thesis.pdf and defense\slides.pdf
pause
