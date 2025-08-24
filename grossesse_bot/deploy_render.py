#!/usr/bin/env python
"""
Script de déploiement automatique sur Render.com
BEAUCOUP PLUS SIMPLE QUE VERCEL !
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def check_git_status():
    """Vérifie le statut Git"""
    print("🔍 Vérification du statut Git...")
    
    try:
        # Vérifier si on est dans un repo Git
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Pas de repository Git trouvé")
            print("💡 Initialisez Git : git init && git add . && git commit -m 'Initial commit'")
            return False
        
        print("✅ Repository Git trouvé")
        return True
        
    except FileNotFoundError:
        print("❌ Git non installé")
        print("💡 Installez Git depuis https://git-scm.com/")
        return False

def check_github_remote():
    """Vérifie si le repo est sur GitHub"""
    print("🔍 Vérification du remote GitHub...")
    
    try:
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if 'github.com' not in result.stdout:
            print("❌ Pas de remote GitHub trouvé")
            print("💡 Ajoutez votre repo GitHub : git remote add origin https://github.com/USER/REPO.git")
            return False
        
        print("✅ Remote GitHub trouvé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

def push_to_github():
    """Pousse les changements sur GitHub"""
    print("📤 Push sur GitHub...")
    
    try:
        # Ajouter tous les fichiers
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit
        subprocess.run(['git', 'commit', '-m', 'Deploy to Render.com'], check=True)
        
        # Push
        subprocess.run(['git', 'push'], check=True)
        
        print("✅ Changements poussés sur GitHub")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Git : {e}")
        return False

def open_render():
    """Ouvre Render.com dans le navigateur"""
    print("🌐 Ouverture de Render.com...")
    
    try:
        webbrowser.open('https://render.com')
        print("✅ Render.com ouvert dans votre navigateur")
        print("\n📋 Étapes à suivre :")
        print("1. Connectez-vous avec GitHub")
        print("2. Cliquez 'New +' → 'Web Service'")
        print("3. Sélectionnez votre repo")
        print("4. Render détectera automatiquement le render.yaml")
        print("5. Cliquez 'Create Web Service'")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        print("💡 Ouvrez manuellement https://render.com")

def create_quick_deploy():
    """Crée un script de déploiement rapide"""
    script_content = """#!/bin/bash
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
"""

    with open("deploy_render.sh", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    # Rendre exécutable (Unix/Linux)
    try:
        os.chmod("deploy_render.sh", 0o755)
    except:
        pass
    
    print("📝 Script de déploiement créé : deploy_render.sh")

def main():
    """Fonction principale"""
    print("🚀 SCRIPT DE DÉPLOIEMENT RENDER.COM")
    print("=" * 50)
    print("🎯 BEAUCOUP PLUS SIMPLE QUE VERCEL !")
    print("=" * 50)
    
    # Vérifications
    if not check_git_status():
        sys.exit(1)
    
    if not check_github_remote():
        sys.exit(1)
    
    # Push sur GitHub
    if push_to_github():
        print("\n🎉 SUCCÈS ! Votre code est sur GitHub")
        print("\n🌐 Prochaines étapes :")
        print("1. Allez sur https://render.com")
        print("2. Connectez-vous avec GitHub")
        print("3. Créez un nouveau Web Service")
        print("4. Sélectionnez votre repo")
        print("5. Render détectera automatiquement le render.yaml")
        print("6. Cliquez 'Create Web Service'")
        
        # Créer le script de déploiement
        create_quick_deploy()
        
        # Demander si on veut ouvrir Render
        response = input("\n❓ Voulez-vous ouvrir Render.com maintenant ? (o/n) : ")
        if response.lower() in ['o', 'oui', 'y', 'yes']:
            open_render()
    
    else:
        print("\n❌ Échec du push sur GitHub")
        print("💡 Vérifiez vos permissions et votre remote")

if __name__ == "__main__":
    main()

