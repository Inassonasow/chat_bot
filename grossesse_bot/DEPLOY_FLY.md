# 🚀 Déploiement sur Fly.io (PLUS STABLE ET FIABLE !)

## 🎯 **Pourquoi Fly.io ?**

- ✅ **Limite : 3 GB** (12x plus que Vercel !)
- ✅ **Très stable** (pas de "déraillage" comme Railway)
- ✅ **Performance excellente**
- ✅ **Déploiement global**
- ✅ **Support Python natif**
- ✅ **Base de données incluse**

## 📋 **Prérequis**

1. **Compte GitHub** avec votre projet `chatbot`
2. **Compte Fly.io** (gratuit)
3. **Fly CLI** installé
4. **Projet Django** fonctionnel localement

## 🔧 **Installation de Fly CLI**

### **Windows (PowerShell) :**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

### **macOS/Linux :**
```bash
curl -L https://fly.io/install.sh | sh
```

## 🚀 **Étapes de déploiement**

### **1. Préparer le projet**

Votre `requirements.txt` doit contenir :

```txt
Django>=5.0
djangorestframework>=3.14
scikit-learn>=1.3
joblib>=1.3
pandas>=2.0
numpy>=1.24
gunicorn>=20.1.0
whitenoise>=6.0.0
```

### **2. Les fichiers de configuration**

- **`fly.toml`** : Configuration Fly.io (déjà créé)
- **`Dockerfile`** : Container Docker (déjà créé)

### **3. Déployer sur Fly.io**

#### **Étape 1 : Connexion**
```bash
fly auth login
```

#### **Étape 2 : Déploiement**
```bash
fly deploy
```

**C'est tout !** 🎉

### **4. Attendre le déploiement**

- **Build** : 3-5 minutes
- **Déploiement** : 1-2 minutes
- **URL** : `https://chatbot-grossesse.fly.dev`

## 🌐 **Votre URL sera :**

```
https://chatbot-grossesse.fly.dev
```

## 📱 **Test de l'API**

Une fois déployé, testez :

```bash
# Test de santé
curl https://chatbot-grossesse.fly.dev/health

# Test du chatbot
curl -X POST https://chatbot-grossesse.fly.dev/chatbot/api/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour, j\'ai des nausées"}'
```

## 🔄 **Déploiement automatique**

À chaque push sur GitHub :
1. **Fly.io détecte** les changements
2. **Rebuild automatiquement** l'application
3. **Redéploie** en quelques minutes
4. **Zéro intervention** de votre part !

## 🆚 **Comparaison Fly.io vs Railway vs Render vs Vercel**

| Aspect | Vercel | Render | Railway | Fly.io |
|--------|--------|--------|---------|--------|
| **Limite taille** | 250 MB ❌ | 500 MB ✅ | 1 GB ✅ | 3 GB ✅ |
| **Stabilité** | Moyenne ✅ | Bonne ✅ | Problématique ❌ | Excellente ✅ |
| **Déploiement** | Complexe ❌ | Simple ✅ | Simple ✅ | Très simple ✅ |
| **Python** | Serverless ❌ | Natif ✅ | Natif ✅ | Natif ✅ |
| **Base de données** | Non ❌ | Oui ✅ | Oui ✅ | Oui ✅ |
| **Performance** | Moyenne ✅ | Bonne ✅ | Bonne ✅ | Excellente ✅ |
| **Gratuit** | Oui ✅ | Oui ✅ | Oui ✅ | Oui ✅ |

## 🎉 **Avantages de Fly.io**

1. **Plus de limite de taille** - 3 GB suffit largement !
2. **Stabilité maximale** - Pas de "déraillage" !
3. **Performance excellente** - Serveurs dédiés
4. **Déploiement global** - Plusieurs régions
5. **Support Python natif** - Pas de contraintes
6. **Base de données incluse** - PostgreSQL gratuit

## 🚨 **En cas de problème**

- **Logs** : `fly logs`
- **Status** : `fly status`
- **Variables d'environnement** : `fly secrets`
- **Support** : Documentation excellente et communauté active

## 🔧 **Commandes utiles**

```bash
# Voir les logs
fly logs

# Voir le status
fly status

# Redémarrer l'app
fly apps restart

# Ouvrir l'app
fly open

# Voir les variables d'environnement
fly secrets list
```

---

## 🎯 **Conclusion**

**Fly.io est la solution la plus stable et fiable !**
- **12x plus généreux** que Vercel (3 GB vs 250 MB)
- **Plus stable** que Railway et Render
- **Performance excellente**
- **Déploiement ultra-simple**

**Votre chatbot sera en ligne en 5 minutes !** 🚀


