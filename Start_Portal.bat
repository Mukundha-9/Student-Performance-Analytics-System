@echo off
title Aditya University - Student Performance Analytics Portal
echo ======================================================================
echo  ADITYA UNIVERSITY - STUDENT PERFORMANCE ANALYTICS SYSTEM
echo  Starting Server and Launching Browser...
echo ======================================================================
cd /d "%~dp0"
start "" http://127.0.0.1:5000
py -3.13 app.py
pause
