@echo off
echo 🚀 Deploiement automatique sur Render...
echo.

echo 📦 Preparation des fichiers...
git add .
git commit -m "🎨 Ajout des couleurs roses et signature Inassona Sow"
git push origin main

echo.
echo ✅ Code pousse sur GitHub !
echo.
echo 🌐 Render va maintenant deployer automatiquement...
echo 📍 Votre app sera accessible sur : https://assistant-grossesse-ia.onrender.com
echo.
echo ⏳ Attendez 5-10 minutes pour le premier deploiement...
echo 🔄 Les prochains deploiements seront plus rapides
echo.
pause
