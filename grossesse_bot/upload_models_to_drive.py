#!/usr/bin/env python
"""
Script pour uploader automatiquement les modèles IA sur Google Drive
"""

import os
import sys
from pathlib import Path
import json

def check_files_exist():
    """Vérifie que les fichiers de modèles existent"""
    print("🔍 Vérification des fichiers de modèles...")
    
    model_files = [
        "model_risque_grossesse.pkl",
        "label_encoders.pkl"
    ]
    
    missing_files = []
    for file in model_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants : {missing_files}")
        print("💡 Assurez-vous d'être dans le bon répertoire")
        return False
    
    print("✅ Tous les fichiers de modèles sont présents")
    return True

def create_upload_instructions():
    """Crée les instructions d'upload manuel"""
    instructions = """
# 📤 Instructions d'Upload sur Google Drive

## 🎯 **Objectif**
Uploadez vos modèles IA sur Google Drive pour respecter la limite Vercel de 250 MB.

## 📁 **Fichiers à uploader**
- `model_risque_grossesse.pkl` (~24 MB)
- `label_encoders.pkl` (~2 MB)

## 🔧 **Étapes d'upload**

### **1. Accéder à Google Drive**
- Allez sur [drive.google.com](https://drive.google.com)
- Connectez-vous avec votre compte Google

### **2. Créer un dossier**
- Clic droit → **Nouveau** → **Dossier**
- Nommez-le : `chatbot-models`

### **3. Upload des modèles**
- Ouvrez le dossier `chatbot-models`
- Glissez-déposez vos fichiers `.pkl`
- Attendez la fin de l'upload

### **4. Rendre les fichiers publics**
- **Clic droit** sur `model_risque_grossesse.pkl`
- **Partager** → **Modifier**
- Changer en **"Tout le monde avec le lien"**
- **Copier le lien**

- **Clic droit** sur `label_encoders.pkl`
- **Partager** → **Modifier**
- Changer en **"Tout le monde avec le lien"**
- **Copier le lien**

### **5. Convertir les liens**
Les liens Google Drive doivent être convertis pour le téléchargement direct.

**Format de conversion :**
- Lien original : `https://drive.google.com/file/d/1ABC123...XYZ/view?usp=sharing`
- Lien de téléchargement : `https://drive.google.com/uc?export=download&id=1ABC123...XYZ`

**Comment extraire l'ID :**
1. Copiez le lien de partage
2. L'ID est entre `/d/` et `/view`
3. Exemple : `1ABC123...XYZ`

## 🔗 **Liens à configurer dans Vercel**

Une fois les liens obtenus, configurez ces variables d'environnement dans Vercel :

```bash
MODEL_URL=https://drive.google.com/uc?export=download&id=VOTRE_ID_MODEL
LABEL_ENCODERS_URL=https://drive.google.com/uc?export=download&id=VOTRE_ID_ENCODEURS
```

## 📱 **Test des liens**

Testez vos liens dans votre navigateur :
1. Collez le lien de téléchargement
2. Vérifiez que le fichier se télécharge
3. Si ça ne marche pas, vérifiez les permissions

## 🚨 **Problèmes courants**

### **Erreur : "Fichier non trouvé"**
- Vérifiez que le fichier est bien partagé
- Vérifiez que le lien est correct

### **Erreur : "Accès refusé"**
- Vérifiez les permissions de partage
- Changez en "Tout le monde avec le lien"

### **Erreur : "Quota dépassé"**
- Google Drive a des limites de téléchargement
- Considérez un autre service (GitHub, AWS S3)

## 🔄 **Après l'upload**

1. **Configurez** les variables d'environnement dans Vercel
2. **Redéployez** : `vercel --prod`
3. **Testez** votre API

## 📚 **Alternatives**

Si Google Drive pose problème :
- **GitHub Releases** : Gratuit, pas de limite de taille
- **AWS S3** : Payant mais professionnel
- **Google Cloud Storage** : Payant mais intégré

---

**🎉 Une fois terminé, votre chatbot respectera la limite Vercel de 250 MB !**
"""
    
    with open("UPLOAD_INSTRUCTIONS.md", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("📝 Instructions d'upload créées : UPLOAD_INSTRUCTIONS.md")

def create_vercel_env_template():
    """Crée un template pour les variables d'environnement Vercel"""
    template = """# 🌐 Variables d'environnement Vercel

# Copiez ce fichier et remplissez les URLs de vos modèles
# Puis ajoutez ces variables dans votre dashboard Vercel

# URL du modèle principal (model_risque_grossesse.pkl)
MODEL_URL=https://drive.google.com/uc?export=download&id=VOTRE_ID_MODEL_ICI

# URL des encodeurs (label_encoders.pkl)
LABEL_ENCODERS_URL=https://drive.google.com/uc?export=download&id=VOTRE_ID_ENCODEURS_ICI

# Exemple avec des IDs fictifs :
# MODEL_URL=https://drive.google.com/uc?export=download&id=1ABC123DEF456GHI789JKL
# LABEL_ENCODERS_URL=https://drive.google.com/uc?export=download&id=1XYZ789ABC123DEF456GHI

# 🔒 IMPORTANT : Ne commitez jamais ce fichier !
# Ajoutez-le à votre .gitignore
"""
    
    with open("vercel.env.template", "w", encoding="utf-8") as f:
        f.write(template)
    
    print("📝 Template des variables d'environnement créé : vercel.env.template")

def create_quick_deploy_script():
    """Crée un script de déploiement rapide"""
    script = """#!/bin/bash
# 🚀 Script de déploiement rapide Vercel

echo "🚀 Déploiement Vercel en cours..."

# Vérifier que vercel CLI est installé
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI non installé. Installation..."
    npm install -g vercel
fi

# Vérifier la connexion
if ! vercel whoami &> /dev/null; then
    echo "🔐 Connexion à Vercel requise..."
    vercel login
fi

# Déployer
echo "📤 Déploiement..."
vercel --prod

echo "✅ Déploiement terminé !"
echo "🌐 Vérifiez votre dashboard Vercel pour l'URL"
"""
    
    with open("deploy_quick.sh", "w", encoding="utf-8") as f:
        f.write(script)
    
    # Rendre le script exécutable (Unix/Linux)
    try:
        os.chmod("deploy_quick.sh", 0o755)
    except:
        pass
    
    print("📝 Script de déploiement rapide créé : deploy_quick.sh")

def main():
    """Fonction principale"""
    print("🚀 SCRIPT DE PRÉPARATION POUR GOOGLE DRIVE")
    print("=" * 50)
    
    # Vérifier les fichiers
    if not check_files_exist():
        print("❌ Fichiers manquants. Arrêt du script.")
        sys.exit(1)
    
    # Créer les instructions
    create_upload_instructions()
    create_vercel_env_template()
    create_quick_deploy_script()
    
    print("\n" + "=" * 50)
    print("🎉 PRÉPARATION TERMINÉE !")
    print("=" * 50)
    print("\n📚 Fichiers créés :")
    print("- UPLOAD_INSTRUCTIONS.md : Instructions détaillées")
    print("- vercel.env.template : Template des variables d'environnement")
    print("- deploy_quick.sh : Script de déploiement rapide")
    print("\n🔧 Prochaines étapes :")
    print("1. Suivez UPLOAD_INSTRUCTIONS.md pour uploader sur Google Drive")
    print("2. Configurez les variables d'environnement dans Vercel")
    print("3. Redéployez avec : ./deploy_quick.sh")
    print("\n💡 Conseil : Commencez par lire UPLOAD_INSTRUCTIONS.md")

if __name__ == "__main__":
    main()


