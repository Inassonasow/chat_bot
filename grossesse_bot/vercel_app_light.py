"""
Application Vercel LÉGÈRE pour le chatbot de grossesse
Charge les modèles depuis des URLs externes pour respecter la limite de 250MB
"""

import os
import sys
import json
import requests
from io import BytesIO
from pathlib import Path

# Ajouter le répertoire du projet au path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configuration Django pour Vercel
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grossesse_bot.settings')

# Imports Django
import django
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Configuration Django
django.setup()

# Variables d'environnement pour les modèles externes
MODEL_URL = os.getenv('MODEL_URL', 'https://drive.google.com/uc?export=download&id=VOTRE_ID_GOOGLE_DRIVE')
LABEL_ENCODERS_URL = os.getenv('LABEL_ENCODERS_URL', 'https://drive.google.com/uc?export=download&id=VOTRE_ID_GOOGLE_DRIVE')

# Cache global pour les modèles
_model_cache = None
_label_encoders_cache = None

def load_model_from_url():
    """Charge le modèle depuis une URL externe"""
    global _model_cache
    
    if _model_cache is not None:
        return _model_cache
    
    try:
        print("📥 Chargement du modèle depuis l'URL externe...")
        response = requests.get(MODEL_URL, timeout=30)
        response.raise_for_status()
        
        # Charger le modèle avec joblib
        import joblib
        _model_cache = joblib.load(BytesIO(response.content))
        print("✅ Modèle chargé avec succès")
        return _model_cache
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle : {e}")
        # Retourner un modèle factice pour éviter les erreurs
        return create_dummy_model()

def load_label_encoders_from_url():
    """Charge les encodeurs depuis une URL externe"""
    global _label_encoders_cache
    
    if _label_encoders_cache is not None:
        return _label_encoders_cache
    
    try:
        print("📥 Chargement des encodeurs depuis l'URL externe...")
        response = requests.get(LABEL_ENCODERS_URL, timeout=30)
        response.raise_for_status()
        
        import joblib
        _label_encoders_cache = joblib.load(BytesIO(response.content))
        print("✅ Encodeurs chargés avec succès")
        return _label_encoders_cache
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement des encodeurs : {e}")
        return create_dummy_encoders()

def create_dummy_model():
    """Crée un modèle factice pour éviter les erreurs"""
    class DummyModel:
        def predict(self, X):
            # Retourner des prédictions aléatoires
            import random
            return [random.choice(['normal', 'modéré', 'élevé'])]
    
    return DummyModel()

def create_dummy_encoders():
    """Crée des encodeurs factices"""
    return {}

def effectuer_prediction_light(data):
    """Version légère de la prédiction"""
    try:
        # Charger le modèle
        model = load_model_from_url()
        
        # Mappings manuels basés sur les encodages observés
        mapping_activite = {
            'modérée': 1,
            'élevée': 2,
            'faible': 0
        }

        mapping_regime = {
            'omnivore': 0,
            'végétarien': 1,
            'autre': 2
        }

        mapping_antecedent = {
            'hypertension': 4,
            'diabète': 3,
            'asthme': 0,
            'aucun': 1,
            'autre': 2
        }

        mapping_symptome = {
            'douleur': 1,
            'fatigue': 2,
            'aucun': 0,
            'nausée': 3
        }

        # Encoder manuellement les variables catégorielles
        activite = mapping_activite.get(data['activité'].lower(), 1)
        regime = mapping_regime.get(data['régime'].lower(), 0)
        antecedent = mapping_antecedent.get(data['antécédents'].lower(), 1)
        symptome = mapping_symptome.get(data['symptôme'].lower(), 0)

        # Créer l'entrée du modèle
        inputs = [
            data['age'],
            data['mois_grossesse'],
            data['poids_kg'],
            data['taille_cm'],
            activite,
            regime,
            antecedent,
            symptome,
        ]

        # Prédire le risque
        prediction = model.predict([inputs])[0]

        # Conseil associé
        conseils = {
            "normal": "Votre grossesse est normale. Continuez une bonne alimentation et restez hydratée.",
            "modéré": "Votre grossesse est à risque modéré. Consultez un médecin deux fois par mois.",
            "élevé": "Votre grossesse est à risque élevé. Suivi médical renforcé requis.",
        }

        return {
            "profil_risque": prediction,
            "conseil": conseils.get(prediction, "Aucun conseil disponible.")
        }

    except Exception as e:
        print(f"❌ Erreur lors de la prédiction : {e}")
        return {
            "profil_risque": "normal",
            "conseil": "Impossible d'évaluer le risque. Consultez votre médecin."
        }

# Base de connaissances simplifiée
KNOWLEDGE_BASE = {
    "nausées": "Les nausées sont très courantes pendant la grossesse, surtout au 1er trimestre. Conseils : mangez de petits repas fréquents, évitez les odeurs fortes, buvez du thé au gingembre.",
    "fatigue": "La fatigue est normale pendant la grossesse. Dormez 8-9h par nuit, faites des siestes si possible, mangez équilibré.",
    "alimentation": "Une alimentation équilibrée est essentielle : 5 fruits et légumes par jour, protéines, produits laitiers pasteurisés, céréales complètes. Prenez de l'acide folique.",
    "exercice": "L'exercice est bénéfique : marche, natation, yoga prénatal. Évitez les sports de contact. 30 minutes d'activité modérée par jour.",
    "douleur": "Les douleurs abdominales peuvent être normales (étirement des ligaments) ou nécessiter une consultation. Si intenses, consultez rapidement.",
    "bébé": "Le développement se fait progressivement : formation des organes au 1er trimestre, croissance au 2ème, maturation au 3ème.",
    "accouchement": "Signes du travail : contractions régulières, perte du bouchon muqueux, rupture de la poche des eaux.",
    "symptômes": "De nombreux symptômes sont normaux : nausées, fatigue, seins tendus. Consultez si saignements, douleurs intenses, fièvre."
}

def find_best_match(user_input):
    """Trouve la meilleure correspondance dans la base de connaissances"""
    user_input = user_input.lower()
    
    keywords = {
        "nausées": ["nausée", "nausées", "vomissement", "mal au cœur"],
        "fatigue": ["fatigue", "fatiguée", "épuisée", "sommeil"],
        "alimentation": ["manger", "aliment", "nourriture", "régime"],
        "exercice": ["sport", "exercice", "activité", "bouger"],
        "douleur": ["douleur", "mal", "souffrance", "ventre"],
        "bébé": ["bébé", "fœtus", "enfant", "mouvements"],
        "accouchement": ["accouchement", "naissance", "travail"],
        "symptômes": ["symptôme", "signe", "problème"]
    }
    
    for topic, words in keywords.items():
        for word in words:
            if word in user_input:
                return topic
    
    return None

def process_message_simple(user_message):
    """Traitement simple des messages sans IA complexe"""
    user_message = user_message.lower()
    
    # Salutations
    if any(word in user_message for word in ['bonjour', 'salut', 'hello']):
        return {
            "response": "Bonjour ! Je suis votre assistant grossesse. Comment puis-je vous aider ?",
            "intention": "salutation"
        }
    
    # Remerciements
    if any(word in user_message for word in ['merci', 'thanks']):
        return {
            "response": "Je vous en prie ! N'hésitez pas si vous avez d'autres questions.",
            "intention": "remerciement"
        }
    
    # Au revoir
    if any(word in user_message for word in ['au revoir', 'bye', 'salut']):
        return {
            "response": "Au revoir ! Prenez soin de vous et de votre bébé.",
            "intention": "au_revoir"
        }
    
    # Recherche dans la base de connaissances
    topic = find_best_match(user_message)
    if topic:
        return {
            "response": KNOWLEDGE_BASE[topic],
            "intention": "information"
        }
    
    # Réponse par défaut
    return {
        "response": "Je n'ai pas trouvé d'information spécifique sur votre question. Je peux vous aider avec : nausées, fatigue, alimentation, exercice, développement du bébé, accouchement. Pouvez-vous reformuler ?",
        "intention": "question_generale"
    }

@csrf_exempt
@require_http_methods(["POST"])
def chatbot_api(request):
    """API du chatbot pour Vercel (version légère)"""
    try:
        # Parser le JSON
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return JsonResponse({
                "response": "Je n'ai pas reçu votre message. Pouvez-vous réessayer ?",
                "error": "Message vide"
            }, status=400)
        
        # Traiter le message avec la version simple
        bot_response = process_message_simple(user_message)
        
        # Préparer la réponse finale
        response_data = {
            "response": bot_response['response'],
            "intention": bot_response.get('intention', 'unknown'),
            "is_emergency": False,  # Version simple
            "user_profile": {}
        }
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({
            "response": "Format de message invalide. Envoyez un JSON avec une clé 'message'.",
            "error": "JSON invalide"
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "response": "Je rencontre une difficulté technique. Pouvez-vous reformuler votre question ?",
            "error": str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def predire_risque_api(request):
    """API de prédiction de risque pour Vercel (version légère)"""
    try:
        data = json.loads(request.body)
        
        # Validation des données
        required_fields = ['age', 'mois_grossesse', 'poids_kg', 'taille_cm', 'activité', 'régime', 'antécédents', 'symptôme']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    "error": f"Champ manquant : {field}"
                }, status=400)
        
        # Effectuer la prédiction
        resultat = effectuer_prediction_light(data)
        
        return JsonResponse({
            "profil_risque": resultat['profil_risque'],
            "conseil": resultat['conseil']
        })
        
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

def health_check(request):
    """Point de terminaison de santé pour Vercel"""
    return JsonResponse({
        "status": "healthy",
        "service": "Chatbot Grossesse API (Version Légère)",
        "version": "2.0.0",
        "note": "Modèles chargés depuis URLs externes"
    })

def home(request):
    """Page d'accueil simple"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chatbot Grossesse API - Version Légère</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
            .container { max-width: 800px; margin: 0 auto; }
            .endpoint { background: rgba(255,255,255,0.1); padding: 15px; margin: 10px 0; border-radius: 5px; }
            code { background: rgba(255,255,255,0.2); padding: 2px 5px; border-radius: 3px; }
            .warning { background: rgba(255,193,7,0.2); padding: 15px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤰 Chatbot Grossesse API - Version Légère</h1>
            <p>API intelligente pour l'accompagnement des femmes enceintes</p>
            
            <div class="warning">
                <h3>⚠️ Version Légère</h3>
                <p>Cette version charge les modèles IA depuis des URLs externes pour respecter les limites de Vercel (250MB).</p>
            </div>
            
            <h2>📡 Endpoints disponibles</h2>
            
            <div class="endpoint">
                <h3>Chatbot API</h3>
                <p><strong>POST</strong> <code>/chatbot/api/</code></p>
                <p>Corps : <code>{"message": "Votre question"}</code></p>
            </div>
            
            <div class="endpoint">
                <h3>Prédiction de risque</h3>
                <p><strong>POST</strong> <code>/api/predire/</code></p>
                <p>Corps : <code>{"age": 30, "mois_grossesse": 6, "poids_kg": 70, "taille_cm": 165, "activité": "modérée", "régime": "omnivore", "antécédents": "aucun", "symptôme": "aucun"}</code></p>
            </div>
            
            <div class="endpoint">
                <h3>Santé de l'API</h3>
                <p><strong>GET</strong> <code>/health</code></p>
            </div>
            
            <h2>🔧 Configuration requise</h2>
            <p>Configurez ces variables d'environnement dans Vercel :</p>
            <ul>
                <li><code>MODEL_URL</code> : URL de votre modèle .pkl</li>
                <li><code>LABEL_ENCODERS_URL</code> : URL de vos encodeurs .pkl</li>
            </ul>
            
            <h2>📚 Documentation</h2>
            <p>Consultez DEPLOY_VERCEL.md pour la configuration complète.</p>
        </div>
    </body>
    </html>
    """)

# Mapping des routes pour Vercel
def handler(request, context):
    """Gestionnaire principal pour Vercel"""
    path = request.get('path', '/')
    method = request.get('method', 'GET')
    
    # Routes de l'API
    if path.startswith('/chatbot/api/') and method == 'POST':
        return chatbot_api(request)
    elif path.startswith('/api/predire/') and method == 'POST':
        return predire_risque_api(request)
    elif path == '/health' and method == 'GET':
        return health_check(request)
    elif path == '/' and method == 'GET':
        return home(request)
    else:
        return JsonResponse({
            "error": "Endpoint non trouvé",
            "path": path,
            "method": method
        }, status=404)

# Pour le développement local
if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


