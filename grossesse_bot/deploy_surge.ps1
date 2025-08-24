# 🤰 Script de déploiement Surge pour l'Assistant Grossesse IA
# =============================================================

Write-Host "🤰 Déploiement de l'Assistant Grossesse IA sur Surge" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier que Python est installé
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    Write-Host "Veuillez installer Python depuis https://python.org" -ForegroundColor Yellow
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

# Vérifier que Surge est installé
try {
    $surgeVersion = surge --version 2>&1
    Write-Host "✅ Surge détecté: $surgeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Surge n'est pas installé" -ForegroundColor Red
    Write-Host "Installation de Surge..." -ForegroundColor Yellow
    npm install -g surge
}

Write-Host ""
Write-Host "📁 Création de l'application statique..." -ForegroundColor Yellow
python surge_app.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de la création de l'application" -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

Write-Host ""
Write-Host "🌐 Déploiement sur Surge..." -ForegroundColor Yellow
Set-Location surge_build
surge

Write-Host ""
Write-Host "✅ Déploiement terminé !" -ForegroundColor Green
Write-Host "🌍 Votre application est maintenant en ligne !" -ForegroundColor Green
Write-Host ""

# Retourner au répertoire parent
Set-Location ..

Read-Host "Appuyez sur Entrée pour quitter"
