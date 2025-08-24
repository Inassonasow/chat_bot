# 📁 Guide d'Hébergement des Modèles IA

Ce guide vous explique comment héberger vos modèles IA volumineux sur Google Drive et les utiliser avec Vercel.

## 🚨 **Problème identifié :**

Vercel a une limite de **250 MB** pour les fonctions serverless. Vos modèles IA dépassent cette limite :
- `model_risque_grossesse.pkl` : ~24 MB
- `label_encoders.pkl` : ~2 MB
- Dépendances (scikit-learn, pandas, numpy) : ~200+ MB

## 🌐 **Solution : Hébergement externe des modèles**

### **Option 1 : Google Drive (Gratuit et simple)**

#### **Étape 1 : Upload des modèles sur Google Drive**

1. **Allez sur [drive.google.com](https://drive.google.com)**
2. **Créez un dossier** `chatbot-models`
3. **Uploadez vos fichiers** :
   - `model_risque_grossesse.pkl`
   - `label_encoders.pkl`

#### **Étape 2 : Rendre les fichiers publics**

1. **Clic droit** sur chaque fichier
2. **Partager** → **Modifier**
3. **Changer en "Tout le monde avec le lien"**
4. **Copier le lien de partage**

#### **Étape 3 : Convertir en lien de téléchargement direct**

Les liens Google Drive doivent être convertis pour le téléchargement direct :

**Format :** `https://drive.google.com/uc?export=download&id=ID_DU_FICHIER`

**Comment obtenir l'ID :**
- Lien original : `https://drive.google.com/file/d/1ABC123...XYZ/view?usp=sharing`
- ID extrait : `1ABC123...XYZ`
- Lien de téléchargement : `https://drive.google.com/uc?export=download&id=1ABC123...XYZ`

### **Option 2 : GitHub Releases (Alternative)**

1. **Créez un repository GitHub**
2. **Uploadez vos modèles** dans les releases
3. **Utilisez les URLs directes** des releases

### **Option 3 : AWS S3 ou Google Cloud Storage (Professionnel)**

Pour une utilisation en production, considérez :
- **AWS S3** : ~$0.023/GB/mois
- **Google Cloud Storage** : ~$0.020/GB/mois

## 🔧 **Configuration Vercel**

### **Étape 1 : Variables d'environnement**

Dans votre dashboard Vercel, ajoutez :

```bash
MODEL_URL=https://drive.google.com/uc?export=download&id=VOTRE_ID_MODEL
LABEL_ENCODERS_URL=https://drive.google.com/uc?export=download&id=VOTRE_ID_ENCODEURS
```

### **Étape 2 : Redéploiement**

```bash
vercel --prod
```

## 📱 **Test de l'API**

### **Test de santé**
```bash
curl https://votre-projet.vercel.app/health
```

### **Test du chatbot**
```bash
curl -X POST https://votre-projet.vercel.app/chatbot/api/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour, j\'ai des nausées"}'
```

### **Test de prédiction**
```bash
curl -X POST https://votre-projet.vercel.app/api/predire/ \
  -H "Content-Type: application/json" \
  -d '{"age": 30, "mois_grossesse": 6, "poids_kg": 70, "taille_cm": 165, "activité": "modérée", "régime": "omnivore", "antécédents": "aucun", "symptôme": "aucun"}'
```

## 🚨 **Limitations et Solutions**

### **Limitation 1 : Temps de chargement**
- **Problème** : Les modèles se chargent à chaque appel
- **Solution** : Cache global dans l'application

### **Limitation 2 : Dépendance externe**
- **Problème** : Si Google Drive est indisponible
- **Solution** : Modèles factices de secours

### **Limitation 3 : Latence**
- **Problème** : Téléchargement depuis Google Drive
- **Solution** : CDN ou stockage plus proche

## 🔄 **Mise à jour des modèles**

### **Étape 1 : Nouveau modèle**
1. **Entraînez votre nouveau modèle**
2. **Uploadez sur Google Drive**
3. **Mettez à jour l'URL dans Vercel**

### **Étape 2 : Redéploiement**
```bash
vercel --prod
```

## 📊 **Monitoring**

### **Vérifier les logs Vercel**
- **Dashboard Vercel** → **Functions** → **Logs**
- **Surveillez** les erreurs de chargement des modèles

### **Métriques de performance**
- **Temps de réponse** de l'API
- **Taux de succès** des prédictions
- **Utilisation de la mémoire**

## 🎯 **Avantages de cette approche**

✅ **Respecte la limite Vercel** de 250 MB  
✅ **Modèles toujours à jour** (facile à mettre à jour)  
✅ **Gratuit** avec Google Drive  
✅ **Scalable** (pas de limite de taille)  
✅ **Sécurisé** (liens privés possibles)  

## 🚨 **Inconvénients**

❌ **Dépendance externe** (Google Drive)  
❌ **Latence** de chargement des modèles  
❌ **Limites Google Drive** (quotas de téléchargement)  

## 🔒 **Sécurité**

### **Liens privés**
- **Google Drive** : Limitez l'accès aux personnes autorisées
- **Authentification** : Ajoutez une clé API si nécessaire

### **Variables d'environnement**
- **Ne commitez jamais** les URLs des modèles
- **Utilisez** le dashboard Vercel pour les secrets

## 📚 **Ressources utiles**

- [Google Drive API](https://developers.google.com/drive)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [Python requests](https://requests.readthedocs.io/)

## 🆘 **Dépannage**

### **Erreur : Modèle non trouvé**
1. **Vérifiez** l'URL dans les variables d'environnement
2. **Testez** le lien dans votre navigateur
3. **Vérifiez** les permissions Google Drive

### **Erreur : Timeout**
1. **Augmentez** `maxDuration` dans `vercel.json`
2. **Optimisez** la taille des modèles
3. **Utilisez** un CDN plus rapide

### **Erreur : Mémoire insuffisante**
1. **Réduisez** la taille des modèles
2. **Utilisez** des modèles quantifiés
3. **Passez** au plan Pro de Vercel

---

**🎉 Avec cette configuration, votre chatbot respectera la limite de 250 MB de Vercel !**

