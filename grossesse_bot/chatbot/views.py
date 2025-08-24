from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import joblib
import numpy as np
from .serializers import GrossesseInputSerializer

# Charger le modèle
model = joblib.load('grossesse_bot/model_risque_grossesse.pkl')

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

def effectuer_prediction(data):
    try:
        # Encoder manuellement les variables catégorielles
        activite = mapping_activite[data['activité'].lower()]
        regime = mapping_regime[data['régime'].lower()]
        antecedent = mapping_antecedent[data['antécédents'].lower()]
        symptome = mapping_symptome[data['symptôme'].lower()]

        # Créer l’entrée du modèle
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

    except KeyError as e:
        raise ValueError(f"Valeur invalide pour une variable catégorielle : {e}")



@api_view(['POST'])
def predire_risque(request):
    serializer = GrossesseInputSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.validated_data

        try:
            resultat = effectuer_prediction(data)
            return Response(resultat)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    return Response(serializer.errors, status=400)

import re
from .intelligent_chatbot import IntelligentGrossesseChatbot

# Instance globale du chatbot intelligent
intelligent_bot = IntelligentGrossesseChatbot()

@api_view(['POST'])
def chatbot(request):
    user_message = request.data.get('message', '')
    
    if not user_message:
        return Response({"response": "Je n'ai pas reçu votre message. Pouvez-vous réessayer ?"})
    
    try:
        # Traiter le message avec le chatbot intelligent
        bot_response = intelligent_bot.process_message(user_message)
        
        # Si le chatbot indique qu'il faut faire une prédiction de risque
        if bot_response.get('ready_for_prediction'):
            extracted_info = bot_response.get('extracted_info', {})
            
            # Convertir les semaines en mois pour la prédiction
            mois_grossesse = extracted_info.get('semaines', 20) // 4
            
            data = {
                "age": int(extracted_info.get('age', 30)),
                "mois_grossesse": int(mois_grossesse),
                "poids_kg": float(extracted_info.get('poids', 65)),
                "taille_cm": int(extracted_info.get('taille', 170)),
                "activité": "modérée",  # Valeur par défaut
                "régime": "omnivore",
                "antécédents": "aucun",
                "symptôme": "aucun"
            }
            
            # Effectuer la prédiction
            try:
                resultat = effectuer_prediction(data)
                prediction_response = f"\n\n🤖 **Évaluation de votre profil de risque :**\n"
                prediction_response += f"Niveau de risque : **{resultat['profil_risque']}**\n"
                prediction_response += f"Conseil : {resultat['conseil']}\n\n"
                prediction_response += "ℹ️ Cette évaluation est indicative. Consultez toujours votre médecin pour un suivi personnalisé."
                
                bot_response['response'] += prediction_response
                
            except ValueError as e:
                bot_response['response'] += f"\n\n⚠️ Erreur lors de l'évaluation : {str(e)}"
        
        # Préparer la réponse finale
        response_data = {
            "response": bot_response['response'],
            "intention": bot_response.get('intention', 'unknown'),
            "is_emergency": bot_response.get('is_emergency', False),
            "user_profile": bot_response.get('user_profile', {})
        }
        
        # Ajouter un conseil santé aléatoire de temps en temps
        if bot_response.get('intention') not in ['urgence', 'evaluation_risque'] and len(user_message) > 20:
            import random
            if random.random() < 0.3:  # 30% de chance
                health_tip = intelligent_bot.get_health_tips()
                response_data["response"] += f"\n\n💡 **Conseil du jour :** {health_tip}"
        
        return Response(response_data)
        
    except Exception as e:
        return Response({
            "response": "Je rencontre une difficulté technique. Pouvez-vous reformuler votre question ?",
            "error": str(e)
        }, status=500)
def chatbot_page(request):
    return render(request, 'index.html')


inputs = [40, 8, 85, 155, 1, 0, 3, 0]  # Exemple pour le cas avec diabète
prediction = model.predict([inputs])[0]
print(f"Prédiction pour les inputs {inputs} : {prediction}")
