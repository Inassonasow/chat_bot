@echo off
echo ========================================
echo    CHATBOT GROSSESSE - DEMARRAGE
echo ========================================
echo.

echo 1. Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo 2. Verification des migrations...
python manage.py migrate

echo.
echo 3. Demarrage du serveur Django...
echo.
echo Le serveur sera accessible sur: http://127.0.0.1:8000
echo Pour acceder au chatbot: http://127.0.0.1:8000/chatbot/
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.

python manage.py runserver

pause
