# 🚀 Guide de Déploiement sur Render - Assistant Grossesse IA

## 📋 **Prérequis**

- ✅ Compte GitHub avec votre code source
- ✅ Compte Render (gratuit)
- ✅ Application Django fonctionnelle en local

## 🔧 **Étape 1 : Préparation du Code**

### **1.1 Créer un fichier `requirements.txt`**
```bash
pip freeze > requirements.txt
```

### **1.2 Créer un fichier `build.sh`**
```bash
#!/usr/bin/env bash
# build.sh
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

### **1.3 Créer un fichier `render.yaml`**
```yaml
services:
  - type: web
    name: assistant-grossesse-ia
    env: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn grossesse_bot.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.16
      - key: DJANGO_SETTINGS_MODULE
        value: grossesse_bot.settings
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: false
      - key: ALLOWED_HOSTS
        value: ".onrender.com"
```

## 🌐 **Étape 2 : Déploiement sur Render**

### **2.1 Créer un compte Render**
1. Allez sur [render.com](https://render.com)
2. Créez un compte gratuit
3. Connectez-vous

### **2.2 Connecter votre repository GitHub**
1. Cliquez sur "New +"
2. Sélectionnez "Web Service"
3. Connectez votre repository GitHub
4. Sélectionnez le repository `Grossesse_chat`

### **2.3 Configuration du service**
- **Name** : `assistant-grossesse-ia`
- **Environment** : `Python 3`
- **Build Command** : `./build.sh`
- **Start Command** : `gunicorn grossesse_bot.wsgi:application`
- **Plan** : `Free`

### **2.4 Variables d'environnement**
- `PYTHON_VERSION` : `3.9.16`
- `DJANGO_SETTINGS_MODULE` : `grossesse_bot.settings`
- `SECRET_KEY` : Généré automatiquement
- `DEBUG` : `false`
- `ALLOWED_HOSTS` : `.onrender.com`

## 🔄 **Étape 3 : Déploiement Automatique**

### **3.1 Push sur GitHub**
```bash
git add .
git commit -m "Préparation pour déploiement Render"
git push origin main
```

### **3.2 Render déploie automatiquement**
- Chaque push déclenche un nouveau déploiement
- Vous pouvez voir les logs en temps réel
- L'URL sera : `https://assistant-grossesse-ia.onrender.com`

## 🎨 **Étape 4 : Personnalisation (Couleurs Roses + Signature)**

### **4.1 Modifier le CSS pour les couleurs roses**
```css
:root {
    --primary-color: #ff69b4;      /* Rose vif */
    --secondary-color: #c71585;    /* Rose sombre */
    --accent-color: #ffb6c1;       /* Rose clair */
    --bg-primary: #ffffff;
    --bg-secondary: #fff0f5;       /* Rose très clair */
    --border-color: #ffc0cb;       /* Rose clair */
}
```

### **4.2 Ajouter votre signature**
```html
<footer class="footer">
    <p>🤰 Assistant Grossesse IA - Développé avec ❤️ pour les futures mamans</p>
    <p><strong>👩‍💻 Développé par : Inassona Sow</strong></p>
</footer>
```

## ✅ **Avantages de Render vs Surge**

| Fonctionnalité | Render | Surge |
|----------------|--------|-------|
| **Django** | ✅ Support complet | ❌ Pas de support |
| **Python** | ✅ Support complet | ❌ Pas de support |
| **Base de données** | ✅ PostgreSQL inclus | ❌ Pas de base de données |
| **Chatbot IA** | ✅ Fonctionne | ❌ Simulation uniquement |
| **Déploiement automatique** | ✅ GitHub | ✅ GitHub |
| **Gratuit** | ✅ 750h/mois | ✅ Illimité |
| **HTTPS** | ✅ Automatique | ✅ Automatique |

## 🧪 **Test du Déploiement**

### **5.1 Vérifier l'URL**
- Votre app sera accessible sur : `https://assistant-grossesse-ia.onrender.com`
- Le chatbot fonctionnera exactement comme en local
- Les couleurs roses seront visibles
- Votre signature sera affichée

### **5.2 Tester les fonctionnalités**
- ✅ Chatbot avec IA
- ✅ Évaluation des risques
- ✅ Interface en couleurs roses
- ✅ Signature "Inassona Sow"

## 🔧 **Dépannage**

### **Erreur de build**
- Vérifiez `requirements.txt`
- Vérifiez `build.sh` (permissions d'exécution)

### **Erreur de démarrage**
- Vérifiez `startCommand`
- Vérifiez les variables d'environnement

### **Erreur de base de données**
- Vérifiez les migrations
- Vérifiez les modèles

## 📚 **Ressources**

- [Documentation Render](https://render.com/docs)
- [Déploiement Django sur Render](https://render.com/docs/deploy-django)
- [Variables d'environnement](https://render.com/docs/environment-variables)

## 🎯 **Prochaines Étapes**

1. **Déployer sur Render** (ce guide)
2. **Ajouter les couleurs roses** (CSS)
3. **Ajouter votre signature** (HTML)
4. **Tester en ligne**
5. **Partager l'URL** 🌍✨

---

**🚀 Votre Assistant Grossesse IA sera bientôt accessible partout dans le monde !**

