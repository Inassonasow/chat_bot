#!/usr/bin/env python
"""
Script de déploiement automatique sur Vercel
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def run_command(command, description):
    """Exécute une commande et gère les erreurs"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Succès")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erreur")
        print(f"Commande : {command}")
        print(f"Erreur : {e.stderr}")
        return None

def check_prerequisites():
    """Vérifie les prérequis"""
    print("🔍 Vérification des prérequis...")
    
    # Vérifier Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        return False
    
    # Vérifier pip
    if not run_command("pip --version", "Vérification de pip"):
        return False
    
    # Vérifier git
    if not run_command("git --version", "Vérification de git"):
        return False
    
    # Vérifier Node.js (pour Vercel CLI)
    if not run_command("node --version", "Vérification de Node.js"):
        print("⚠️  Node.js requis pour Vercel CLI")
        return False
    
    # Vérifier npm
    if not run_command("npm --version", "Vérification de npm"):
        return False
    
    print("✅ Tous les prérequis sont satisfaits")
    return True

def install_dependencies():
    """Installe les dépendances Vercel"""
    print("📦 Installation des dépendances...")
    
    # Installer les dépendances Python
    if not run_command("pip install -r requirements-vercel.txt", "Installation des dépendances Python"):
        return False
    
    # Installer Vercel CLI globalement
    if not run_command("npm install -g vercel", "Installation de Vercel CLI"):
        return False
    
    return True

def test_vercel_app():
    """Teste l'application Vercel localement"""
    print("🧪 Test de l'application Vercel...")
    
    # Vérifier que vercel_app.py existe
    if not Path("vercel_app.py").exists():
        print("❌ vercel_app.py non trouvé")
        return False
    
    # Test simple d'import
    try:
        import vercel_app
        print("✅ Import de vercel_app.py réussi")
        return True
    except Exception as e:
        print(f"❌ Erreur d'import : {e}")
        return False

def deploy_to_vercel():
    """Déploie sur Vercel"""
    print("🚀 Déploiement sur Vercel...")
    
    # Vérifier si déjà connecté
    if not run_command("vercel whoami", "Vérification de la connexion Vercel"):
        print("🔐 Connexion à Vercel requise...")
        if not run_command("vercel login", "Connexion à Vercel"):
            return False
    
    # Déployer
    print("📤 Déploiement en cours...")
    deploy_result = run_command("vercel --yes", "Déploiement sur Vercel")
    
    if deploy_result:
        print("✅ Déploiement réussi !")
        # Extraire l'URL du déploiement
        if "Preview:" in deploy_result:
            url = deploy_result.split("Preview:")[1].split()[0]
            print(f"🌐 URL de prévisualisation : {url}")
        if "Production:" in deploy_result:
            url = deploy_result.split("Production:")[1].split()[0]
            print(f"🌐 URL de production : {url}")
        return True
    else:
        print("❌ Déploiement échoué")
        return False

def create_deployment_summary():
    """Crée un résumé du déploiement"""
    summary = """
# 📋 Résumé du Déploiement Vercel

## ✅ Étapes accomplies
- [x] Vérification des prérequis
- [x] Installation des dépendances
- [x] Test de l'application
- [x] Déploiement sur Vercel

## 🔗 URLs importantes
- **Dashboard Vercel** : https://vercel.com/dashboard
- **Documentation** : https://vercel.com/docs

## 📱 Test de l'API
```bash
# Test de santé
curl https://votre-projet.vercel.app/health

# Test du chatbot
curl -X POST https://votre-projet.vercel.app/chatbot/api/ \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Bonjour"}'
```

## 🚨 Points d'attention
1. **Modèles IA** : Les fichiers .pkl sont trop volumineux pour Vercel
2. **Stockage** : Utilisez un stockage externe pour les modèles
3. **Variables d'environnement** : Configurez-les dans le dashboard Vercel

## 🔄 Mise à jour
Pour redéployer après des modifications :
```bash
vercel --prod
```

## 📊 Monitoring
- Surveillez les performances dans le dashboard Vercel
- Vérifiez les logs d'erreur
- Testez régulièrement vos endpoints
"""
    
    with open("DEPLOYMENT_SUMMARY.md", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("📝 Résumé du déploiement créé : DEPLOYMENT_SUMMARY.md")

def main():
    """Fonction principale"""
    print("🚀 SCRIPT DE DÉPLOIEMENT VERCEL")
    print("=" * 50)
    
    # Vérifier les prérequis
    if not check_prerequisites():
        print("❌ Prérequis non satisfaits. Arrêt du déploiement.")
        sys.exit(1)
    
    # Installer les dépendances
    if not install_dependencies():
        print("❌ Échec de l'installation des dépendances.")
        sys.exit(1)
    
    # Tester l'application
    if not test_vercel_app():
        print("❌ Échec du test de l'application.")
        sys.exit(1)
    
    # Déployer
    if not deploy_to_vercel():
        print("❌ Échec du déploiement.")
        sys.exit(1)
    
    # Créer le résumé
    create_deployment_summary()
    
    print("\n" + "=" * 50)
    print("🎉 DÉPLOIEMENT TERMINÉ AVEC SUCCÈS !")
    print("=" * 50)
    print("\n📚 Consultez DEPLOYMENT_SUMMARY.md pour plus d'informations")
    print("🌐 Vérifiez votre dashboard Vercel pour l'URL de production")

if __name__ == "__main__":
    main()


