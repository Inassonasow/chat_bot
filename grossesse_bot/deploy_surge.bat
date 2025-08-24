@echo off
echo 🤰 Deploiement de l'Assistant Grossesse IA sur Surge
echo ===================================================
echo.

echo 📁 Creation de l'application statique...
python surge_app.py

echo.
echo 🌐 Deploiement sur Surge...
cd surge_build
surge

echo.
echo ✅ Deploiement termine !
echo 🌍 Votre application est maintenant en ligne !
echo.
pause
