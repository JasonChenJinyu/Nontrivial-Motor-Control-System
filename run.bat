@echo off
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python Motor_Control_Interface.py
pause
