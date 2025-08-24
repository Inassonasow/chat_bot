#!/usr/bin/env python3
"""
Script de déploiement automatisé pour Render
Assistant Grossesse IA - Inassona Sow
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n🔄 {description}...")
    print(f"📝 Commande: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Succès: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur: {e}")
        print(f"📋 Sortie d'erreur: {e.stderr}")
        return False

def check_git_status():
    """Vérifie le statut Git"""
    print("\n🔍 Vérification du statut Git...")
    
    # Vérifier si on est dans un repo Git
    if not Path(".git").exists():
        print("❌ Pas de repository Git détecté")
        return False
    
    # Vérifier le statut
    status = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    
    if status.stdout.strip():
        print("📝 Fichiers modifiés détectés:")
        print(status.stdout)
        return True
    else:
        print("✅ Aucun fichier modifié")
        return False

def deploy_to_render():
    """Déploie l'application sur Render"""
    print("\n🚀 Déploiement sur Render...")
    
    # Vérifier que tous les fichiers nécessaires existent
    required_files = [
        "requirements.txt",
        "build.sh", 
        "render.yaml",
        "manage.py",
        "grossesse_bot/settings.py",
        "grossesse_bot/wsgi.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants: {missing_files}")
        return False
    
    print("✅ Tous les fichiers requis sont présents")
    
    # Ajouter tous les fichiers
    if not run_command("git add .", "Ajout des fichiers au staging"):
        return False
    
    # Commit des changements
    commit_message = "🚀 Déploiement automatique sur Render - Assistant Grossesse IA"
    if not run_command(f'git commit -m "{commit_message}"', "Commit des changements"):
        return False
    
    # Push vers GitHub
    if not run_command("git push origin main", "Push vers GitHub"):
        return False
    
    print("\n🎉 Déploiement terminé avec succès !")
    print("🌐 Votre application sera bientôt disponible sur Render")
    print("📱 Surveillez les logs sur votre dashboard Render")
    
    return True

def main():
    """Fonction principale"""
    print("🤰 Assistant Grossesse IA - Déploiement Render")
    print("=" * 50)
    
    # Vérifier le statut Git
    if not check_git_status():
        print("\n❌ Impossible de continuer sans repository Git")
        sys.exit(1)
    
    # Demander confirmation
    response = input("\n❓ Voulez-vous continuer avec le déploiement ? (y/N): ")
    if response.lower() != 'y':
        print("❌ Déploiement annulé")
        sys.exit(0)
    
    # Procéder au déploiement
    if deploy_to_render():
        print("\n🎊 Félicitations ! Votre Assistant Grossesse IA est en cours de déploiement !")
        print("🔗 Surveillez votre dashboard Render pour l'URL finale")
    else:
        print("\n💥 Le déploiement a échoué. Vérifiez les erreurs ci-dessus.")
        sys.exit(1)

if __name__ == "__main__":
    main()
