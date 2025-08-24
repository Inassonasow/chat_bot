"""
Configuration du projet Chatbot Grossesse
"""

import os
from pathlib import Path

# Chemins du projet
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model_risque_grossesse.pkl"
LABEL_ENCODERS_PATH = BASE_DIR / "label_encoders.pkl"
DATA_PATH = BASE_DIR / "donnees_grossesse.csv"

# Configuration Django
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-wd&!1c@-g4gb_^$8!*tx$^m1-lj!mnb=dgkx6escx6iw55m(n@')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Configuration de la base de données
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')

# Configuration du serveur
PORT = int(os.getenv('PORT', 8000))
HOST = os.getenv('HOST', '127.0.0.1')

# Configuration IA
MODEL_CONFIG = {
    'model_path': str(MODEL_PATH),
    'label_encoders_path': str(LABEL_ENCODERS_PATH),
    'data_path': str(DATA_PATH)
}

# Configuration des mappings
MAPPING_ACTIVITE = {
    'modérée': 1,
    'élevée': 2,
    'faible': 0
}

MAPPING_REGIME = {
    'omnivore': 0,
    'végétarien': 1,
    'autre': 2
}

MAPPING_ANTECEDENT = {
    'hypertension': 4,
    'diabète': 3,
    'asthme': 0,
    'aucun': 1,
    'autre': 2
}

MAPPING_SYMPTOME = {
    'douleur': 1,
    'fatigue': 2,
    'aucun': 0,
    'nausée': 3
}

# Conseils par niveau de risque
CONSEILS_RISQUE = {
    "normal": "Votre grossesse est normale. Continuez une bonne alimentation et restez hydratée.",
    "modéré": "Votre grossesse est à risque modéré. Consultez un médecin deux fois par mois.",
    "élevé": "Votre grossesse est à risque élevé. Suivi médical renforcé requis.",
}
