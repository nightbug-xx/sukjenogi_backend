@echo off
cd /d C:\sukjenogi
set PYTHONPATH=C:\sukjenogi
call venv\Scripts\activate.bat
python scripts\reset_homeworks.py >> logs\reset.log 2>&1
