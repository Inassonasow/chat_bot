#!/usr/bin/env bash
# build.sh - Script de build pour Render

echo "🚀 Début du build sur Render..."

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Collecter les fichiers statiques
echo "🎨 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Appliquer les migrations
echo "🗄️ Application des migrations..."
python manage.py migrate

echo "✅ Build terminé avec succès !"
