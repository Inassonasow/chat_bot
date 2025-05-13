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

@api_view(['POST'])
def chatbot(request):
    user_message = request.data.get('message', '').lower()

    # Réponses simples pour les salutations
    if 'bonjour' in user_message:
        return Response({"response": "Bonjour ! Comment puis-je vous aider avec votre grossesse ?"})

    # Si l'utilisateur donne des informations sur sa grossesse
    if 'je suis' in user_message or 'j’ai' in user_message:
        try:
            # Extraire dynamiquement les informations de l'utilisateur
            age = re.search(r'(\d+)\s*ans', user_message)
            mois_grossesse = re.search(r'(\d+)\s*mois', user_message)
            poids_kg = re.search(r'(\d+)\s*kg', user_message)
            taille_cm = re.search(r'(\d+)\s*cm', user_message)

            data = {
                "age": int(age.group(1)) if age else 30,  # Valeur par défaut
                "mois_grossesse": int(mois_grossesse.group(1)) if mois_grossesse else 5,
                "poids_kg": float(poids_kg.group(1)) if poids_kg else 65,
                "taille_cm": int(taille_cm.group(1)) if taille_cm else 170,
                "activité": "modérée",  # Valeur par défaut
                "régime": "omnivore",
                "antécédents": "aucun",
                "symptôme": "aucun"
            }

            # Effectuer la prédiction
            resultat = effectuer_prediction(data)

            # Retourner la réponse du chatbot
            return Response({"response": f"Votre grossesse est considérée à risque {resultat['profil_risque']}. {resultat['conseil']}"})

        except ValueError as e:
            return Response({"response": f"Erreur : {str(e)}"})

    # Réponse par défaut
    return Response({"response": "Je suis désolé, je n'ai pas compris. Pouvez-vous reformuler ?"})
    return Response(serializer.errors, status=400)
def chatbot_page(request):
    return render(request, 'index.html')


inputs = [40, 8, 85, 155, 1, 0, 3, 0]  # Exemple pour le cas avec diabète
prediction = model.predict([inputs])[0]
print(f"Prédiction pour les inputs {inputs} : {prediction}")
