"""
Application Vercel pour le chatbot de grossesse
Adaptée pour le déploiement serverless
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire du projet au path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configuration Django pour Vercel
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grossesse_bot.settings')

# Imports Django
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Configuration Django
django.setup()

# Imports de notre application
from chatbot.intelligent_chatbot import IntelligentGrossesseChatbot
from chatbot.views import effectuer_prediction

# Instance globale du chatbot
chatbot = IntelligentGrossesseChatbot()

@csrf_exempt
@require_http_methods(["POST"])
def chatbot_api(request):
    """API du chatbot pour Vercel"""
    try:
        # Parser le JSON
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return JsonResponse({
                "response": "Je n'ai pas reçu votre message. Pouvez-vous réessayer ?",
                "error": "Message vide"
            }, status=400)
        
        # Traiter le message avec le chatbot intelligent
        bot_response = chatbot.process_message(user_message)
        
        # Si le chatbot indique qu'il faut faire une prédiction de risque
        if bot_response.get('ready_for_prediction'):
            extracted_info = bot_response.get('extracted_info', {})
            
            # Convertir les semaines en mois pour la prédiction
            mois_grossesse = extracted_info.get('semaines', 20) // 4
            
            data_for_prediction = {
                "age": int(extracted_info.get('age', 30)),
                "mois_grossesse": int(mois_grossesse),
                "poids_kg": float(extracted_info.get('poids', 65)),
                "taille_cm": int(extracted_info.get('taille', 170)),
                "activité": "modérée",
                "régime": "omnivore",
                "antécédents": "aucun",
                "symptôme": "aucun"
            }
            
            # Effectuer la prédiction
            try:
                resultat = effectuer_prediction(data_for_prediction)
                prediction_response = f"\n\n🤖 **Évaluation de votre profil de risque :**\n"
                prediction_response += f"Niveau de risque : **{resultat['profil_risque']}**\n"
                prediction_response += f"Conseil : {resultat['conseil']}\n\n"
                prediction_response += "ℹ️ Cette évaluation est indicative. Consultez toujours votre médecin pour un suivi personnalisé."
                
                bot_response['response'] += prediction_response
                
            except Exception as e:
                bot_response['response'] += f"\n\n⚠️ Erreur lors de l'évaluation : {str(e)}"
        
        # Préparer la réponse finale
        response_data = {
            "response": bot_response['response'],
            "intention": bot_response.get('intention', 'unknown'),
            "is_emergency": bot_response.get('is_emergency', False),
            "user_profile": bot_response.get('user_profile', {})
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
    """API de prédiction de risque pour Vercel"""
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
        resultat = effectuer_prediction(data)
        
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
        "service": "Chatbot Grossesse API",
        "version": "1.0.0"
    })

def home(request):
    """Page d'accueil simple"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chatbot Grossesse API</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            code { background: #e0e0e0; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤰 Chatbot Grossesse API</h1>
            <p>API intelligente pour l'accompagnement des femmes enceintes</p>
            
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
            
            <h2>🔧 Utilisation</h2>
            <p>Cette API peut être utilisée par des applications mobiles, des sites web ou d'autres services.</p>
            
            <h2>📚 Documentation</h2>
            <p>Pour plus d'informations, consultez le README du projet.</p>
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

