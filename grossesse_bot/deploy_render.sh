#!/bin/bash
# 🚀 Script de déploiement rapide Render

echo "🚀 Déploiement Render en cours..."

# Vérifier Git
if ! git status &> /dev/null; then
    echo "❌ Git non initialisé"
    git init
    git add .
    git commit -m "Initial commit"
fi

# Vérifier GitHub remote
if ! git remote -v | grep github.com &> /dev/null; then
    echo "❌ Remote GitHub manquant"
    echo "💡 Ajoutez : git remote add origin https://github.com/USER/REPO.git"
    exit 1
fi

# Push sur GitHub
echo "📤 Push sur GitHub..."
git add .
git commit -m "Deploy to Render"
git push

echo "✅ Déployé sur GitHub !"
echo "🌐 Allez sur https://render.com pour créer votre service"
echo "📋 Render détectera automatiquement le render.yaml"
