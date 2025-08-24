#!/usr/bin/env bash
# build.sh - Script de build pour Render

set -e  # Arrêter en cas d'erreur

echo "🚀 Début du build sur Render..."
echo "📁 Répertoire de travail: $(pwd)"
echo "🐍 Version Python: $(python --version)"

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Vérifier que Django est installé
echo "✅ Django installé: $(python -c 'import django; print(django.get_version())')"

# Collecter les fichiers statiques
echo "🎨 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# Appliquer les migrations
echo "🗄️ Application des migrations..."
python manage.py migrate --noinput

# Vérifier la configuration
echo "🔍 Vérification de la configuration..."
python manage.py check --deploy

echo "✅ Build terminé avec succès !"
echo "🚀 Prêt pour le démarrage sur Render !"

