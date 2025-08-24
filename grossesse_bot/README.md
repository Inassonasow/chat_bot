# 🤰 Chatbot Grossesse - IA

Un chatbot intelligent spécialisé dans l'évaluation des risques de grossesse, basé sur Django et utilisant un modèle d'intelligence artificielle (Random Forest).

## 🚀 Fonctionnalités

- **Évaluation des risques** de grossesse basée sur 8 paramètres
- **Chatbot intelligent** avec compréhension du langage naturel
- **API REST** pour l'intégration avec d'autres applications
- **Interface web** intuitive et responsive
- **Modèle IA performant** avec 91.26% d'accuracy

## 🛠️ Technologies utilisées

- **Backend :** Django 5.2 + Django REST Framework
- **IA/ML :** Scikit-learn, Random Forest
- **Base de données :** SQLite
- **Frontend :** HTML, CSS, JavaScript
- **Traitement des données :** Pandas, NumPy

## 📋 Prérequis

- Python 3.8+
- pip (gestionnaire de packages Python)

## 🔧 Installation

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd chat_bot/grossesse_bot
```

### 2. Créer un environnement virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations
```bash
python manage.py migrate
```

### 5. Créer un superutilisateur (optionnel)
```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur
```bash
python manage.py runserver
```

## 🌐 Utilisation

### Interface Web
- Ouvrez votre navigateur et allez sur `http://127.0.0.1:8000/chatbot/`
- Interagissez avec le chatbot en tapant vos questions

### API REST
- **Prédiction de risque :** `POST /api/predire/`
- **Chatbot :** `POST /chatbot/api/`

### Exemple d'utilisation de l'API
```python
import requests

# Prédiction de risque
data = {
    "age": 30,
    "mois_grossesse": 6,
    "poids_kg": 70.0,
    "taille_cm": 165.0,
    "activité": "modérée",
    "régime": "omnivore",
    "antécédents": "aucun",
    "symptôme": "aucun"
}

response = requests.post('http://127.0.0.1:8000/api/predire/', json=data)
print(response.json())
```

## 📊 Modèle IA

Le modèle utilise un **Random Forest Classifier** avec les paramètres suivants :
- **Variables d'entrée :** 8 caractéristiques (âge, mois de grossesse, poids, taille, activité, régime, antécédents, symptômes)
- **Sortie :** Classification du risque (normal, modéré, élevé)
- **Performance :** 91.26% d'accuracy

## 🗂️ Structure du projet

```
grossesse_bot/
├── grossesse_bot/          # Configuration Django
│   ├── settings.py         # Paramètres du projet
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuration WSGI
├── chatbot/                # Application principale
│   ├── models.py          # Modèles de données
│   ├── views.py           # Logique métier + IA
│   ├── serializers.py     # Validation des données
│   ├── templates/         # Interface HTML
│   └── static/            # CSS/JS
├── model_risque_grossesse.pkl  # Modèle IA pré-entraîné
├── requirements.txt        # Dépendances Python
└── README.md              # Ce fichier
```

## 🔒 Sécurité

⚠️ **Important :** 
- Changez la clé secrète Django en production
- Ne partagez jamais les fichiers `.pkl` contenant le modèle
- Utilisez des variables d'environnement pour les données sensibles

## 🤝 Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou problème, n'hésitez pas à ouvrir une issue sur GitHub.

---

**Développé avec ❤️ pour la santé des futures mamans**
