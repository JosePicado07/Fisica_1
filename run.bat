@echo off
REM Instala las dependencias (si hacen falta) y corre el simulador.
REM Doble clic en este archivo, o "run.bat" desde una terminal.

python -m pip install -r requirements.txt
python physics_playground.py

pause
