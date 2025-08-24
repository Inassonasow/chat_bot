@echo off
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
echo Environnement virtuel active !
echo.
echo Pour lancer le serveur Django, tapez: python manage.py runserver
echo Pour installer des packages, tapez: pip install nom_du_package
echo.
cmd /k

