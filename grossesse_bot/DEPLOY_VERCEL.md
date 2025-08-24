# 🚀 Guide de Déploiement sur Vercel

Ce guide vous explique comment déployer votre chatbot de grossesse sur Vercel.

## 📋 Prérequis

- Compte Vercel (gratuit sur [vercel.com](https://vercel.com))
- Git installé sur votre machine
- Projet Django configuré

## 🔧 Étape 1 : Préparation du Projet

### 1.1 Installer les dépendances Vercel
```bash
pip install -r requirements-vercel.txt
```

### 1.2 Tester l'application Vercel localement
```bash
python vercel_app.py
```

## 🌐 Étape 2 : Déploiement sur Vercel

### 2.1 Installer Vercel CLI
```bash
npm install -g vercel
```

### 2.2 Se connecter à Vercel
```bash
vercel login
```

### 2.3 Déployer le projet
```bash
vercel
```

Suivez les instructions :
- **Set up and deploy?** → `Y`
- **Which scope?** → Choisissez votre compte
- **Link to existing project?** → `N`
- **Project name** → `chatbot-grossesse` (ou nom de votre choix)
- **In which directory is your code located?** → `./` (répertoire actuel)
- **Want to override the settings?** → `N`

### 2.4 Configuration automatique
Vercel détectera automatiquement que c'est un projet Python et utilisera la configuration de `vercel.json`.

## 📁 Étape 3 : Gestion des Fichiers de Modèles

### 3.1 Problème des modèles .pkl
Les modèles IA (`.pkl`) sont trop volumineux pour Vercel. Solutions :

#### Option A : Stockage externe (Recommandée)
```python
# Dans vercel_app.py, modifier pour charger depuis une URL
import requests

def load_model_from_url():
    model_url = "https://votre-stockage.com/model.pkl"
    response = requests.get(model_url)
    return joblib.load(BytesIO(response.content))
```

#### Option B : Modèles plus petits
- Entraîner des modèles plus légers
- Utiliser des formats comme ONNX ou TensorFlow Lite

#### Option C : API séparée pour les modèles
- Héberger les modèles sur une autre plateforme (Heroku, AWS)
- Appeler cette API depuis Vercel

### 3.2 Configuration des variables d'environnement
Dans le dashboard Vercel, ajoutez :
```
MODEL_URL=https://votre-stockage.com/model.pkl
LABEL_ENCODERS_URL=https://votre-stockage.com/label_encoders.pkl
```

## 🔄 Étape 4 : Déploiement Continu

### 4.1 Connecter Git
```bash
vercel --prod
```

### 4.2 Déploiement automatique
À chaque push sur votre branche principale, Vercel redéploiera automatiquement.

## 🧪 Étape 5 : Test du Déploiement

### 5.1 Vérifier la santé de l'API
```bash
curl https://votre-projet.vercel.app/health
```

### 5.2 Tester le chatbot
```bash
curl -X POST https://votre-projet.vercel.app/chatbot/api/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour, j\'ai des nausées"}'
```

### 5.3 Tester la prédiction
```bash
curl -X POST https://votre-projet.vercel.app/api/predire/ \
  -H "Content-Type: application/json" \
  -d '{"age": 30, "mois_grossesse": 6, "poids_kg": 70, "taille_cm": 165, "activité": "modérée", "régime": "omnivore", "antécédents": "aucun", "symptôme": "aucun"}'
```

## 📊 Étape 6 : Monitoring et Analytics

### 6.1 Dashboard Vercel
- Visites et performances
- Logs d'erreur
- Métriques de déploiement

### 6.2 Logs personnalisés
```python
import logging
logger = logging.getLogger(__name__)

def chatbot_api(request):
    logger.info(f"Message reçu: {request.body}")
    # ... reste du code
```

## 🚨 Problèmes Courants et Solutions

### Problème : Timeout des fonctions
**Solution :** Optimiser le code, réduire la taille des modèles

### Problème : Erreur de mémoire
**Solution :** Utiliser des modèles plus légers, optimiser les imports

### Problème : Modèles trop volumineux
**Solution :** Stockage externe ou API séparée

## 🔒 Sécurité

### Variables d'environnement
- Ne jamais commiter de clés secrètes
- Utiliser le dashboard Vercel pour les secrets

### CORS et authentification
```python
# Dans vercel_app.py
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST"])
def api_endpoint(request):
    # Votre code ici
```

## 📱 Intégration Frontend

### Application web
```javascript
const response = await fetch('https://votre-api.vercel.app/chatbot/api/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: userInput })
});
```

### Application mobile
```python
# L'API est compatible avec toutes les plateformes
# Utilisez les mêmes endpoints
```

## 🎯 Avantages de Vercel

✅ **Gratuit** pour les projets personnels  
✅ **Déploiement automatique** depuis Git  
✅ **CDN global** pour de meilleures performances  
✅ **HTTPS automatique**  
✅ **Monitoring intégré**  
✅ **Scalabilité automatique**  

## 📚 Ressources Utiles

- [Documentation Vercel](https://vercel.com/docs)
- [Déploiement Python sur Vercel](https://vercel.com/docs/runtimes/python)
- [Vercel CLI](https://vercel.com/docs/cli)

## 🆘 Support

En cas de problème :
1. Vérifiez les logs dans le dashboard Vercel
2. Testez localement avec `vercel dev`
3. Consultez la documentation Vercel
4. Posez vos questions sur le forum Vercel

---

**🎉 Félicitations ! Votre chatbot de grossesse est maintenant déployé sur Vercel !**
