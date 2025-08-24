"""
Paramètres Django optimisés pour Vercel
"""

from .settings import *

# Configuration pour Vercel
DEBUG = False
ALLOWED_HOSTS = ['*']  # Vercel gère la sécurité

# Base de données - Utiliser SQLite en mémoire pour Vercel
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Base de données en mémoire
    }
}

# Configuration des fichiers statiques pour Vercel
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Middleware pour servir les fichiers statiques
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Ajouter en premier
] + MIDDLEWARE

# Configuration WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Sécurité pour la production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuration des sessions
SESSION_COOKIE_SECURE = False  # Vercel gère HTTPS
CSRF_COOKIE_SECURE = False

# Logging pour Vercel
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Configuration des modèles IA pour Vercel
# Les modèles seront chargés depuis le stockage Vercel
MODEL_PATH = '/tmp/model_risque_grossesse.pkl'
LABEL_ENCODERS_PATH = '/tmp/label_encoders.pkl'

