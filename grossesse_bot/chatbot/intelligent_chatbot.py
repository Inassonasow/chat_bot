"""
Chatbot intelligent pour la grossesse
Utilise la base de connaissances et le processeur NLP pour répondre à toutes les questions
"""

import random
import json
from typing import Dict, List, Optional, Tuple
from .knowledge_base import GrossesseKnowledgeBase
from .nlp_processor import NLPProcessor

class IntelligentGrossesseChatbot:
    """Chatbot intelligent spécialisé dans la grossesse"""
    
    def __init__(self):
        self.knowledge_base = GrossesseKnowledgeBase()
        self.nlp_processor = NLPProcessor()
        
        # Historique de conversation pour le contexte
        self.conversation_history = []
        self.user_profile = {}
        
        # Réponses par défaut selon l'intention
        self.default_responses = {
            'salutation': [
                "Bonjour ! Je suis votre assistant spécialisé en grossesse. Comment puis-je vous aider aujourd'hui ?",
                "Salut ! Je suis là pour répondre à toutes vos questions sur la grossesse. Que souhaitez-vous savoir ?",
                "Bonjour ! En tant qu'expert en grossesse, je peux vous conseiller sur tous les aspects de cette période. Posez-moi vos questions !"
            ],
            'remerciement': [
                "Je vous en prie ! N'hésitez pas si vous avez d'autres questions.",
                "C'est avec plaisir ! Je suis là pour vous accompagner pendant votre grossesse.",
                "De rien ! Votre bien-être et celui de votre bébé sont importants."
            ],
            'au_revoir': [
                "Au revoir ! Prenez soin de vous et de votre bébé. À bientôt !",
                "À bientôt ! N'hésitez pas à revenir si vous avez des questions.",
                "Bonne journée ! Je reste disponible pour vous accompagner."
            ]
        }
        
        # Conseils personnalisés par trimestre
        self.trimester_advice = {
            'premier_trimestre': {
                'general': "Au 1er trimestre, votre corps s'adapte. Les nausées et la fatigue sont normales.",
                'nutrition': "Prenez de l'acide folique et mangez équilibré malgré les nausées.",
                'precautions': "Évitez l'alcool, le tabac et les médicaments non prescrits."
            },
            'deuxieme_trimestre': {
                'general': "Le 2ème trimestre est souvent le plus agréable. Vous devriez sentir les premiers mouvements.",
                'nutrition': "Augmentez vos apports en fer et calcium. Continuez une alimentation variée.",
                'precautions': "Attention à votre posture et évitez de dormir sur le dos."
            },
            'troisieme_trimestre': {
                'general': "Au 3ème trimestre, préparez-vous à l'accouchement. Le bébé grandit rapidement.",
                'nutrition': "Mangez de petits repas fréquents pour éviter les reflux.",
                'precautions': "Surveillez les contractions et préparez votre valise de maternité."
            }
        }
    
    def update_user_profile(self, extracted_info: Dict):
        """Met à jour le profil utilisateur avec les nouvelles informations"""
        for key, value in extracted_info.items():
            if value is not None:
                self.user_profile[key] = value
    
    def get_personalized_greeting(self) -> str:
        """Génère une salutation personnalisée basée sur le profil"""
        if 'semaines' in self.user_profile:
            weeks = self.user_profile['semaines']
            if weeks <= 12:
                trimester = "1er trimestre"
            elif weeks <= 28:
                trimester = "2ème trimestre"
            else:
                trimester = "3ème trimestre"
            
            return f"Bonjour ! Je vois que vous êtes à {weeks} semaines de grossesse ({trimester}). Comment vous sentez-vous aujourd'hui ?"
        
        return random.choice(self.default_responses['salutation'])
    
    def handle_emergency(self, message_analysis: Dict) -> str:
        """Gère les messages d'urgence"""
        emergency_response = (
            "🚨 ATTENTION : Votre message indique une situation qui pourrait nécessiter une consultation médicale urgente.\n\n"
            "CONTACTEZ IMMÉDIATEMENT :\n"
            "• Votre médecin ou sage-femme\n"
            "• Les urgences maternité de votre hôpital\n"
            "• Le 15 (SAMU) si c'est très urgent\n\n"
            "Signes d'urgence : saignements abondants, douleurs intenses, contractions régulières avant terme, "
            "perte de liquide, fièvre élevée, maux de tête sévères avec troubles visuels.\n\n"
            "En attendant, reposez-vous et ne restez pas seule."
        )
        
        return emergency_response
    
    def handle_symptom_inquiry(self, message_analysis: Dict) -> str:
        """Traite les questions sur les symptômes"""
        medical_info = message_analysis.get('medical_info', {})
        pregnancy_stage = message_analysis.get('pregnancy_stage')
        
        if 'symptome' in medical_info:
            symptom = medical_info['symptome']
            
            # Réponse spécialisée par symptôme
            response = self.knowledge_base.get_response(symptom, message_analysis['cleaned_message'])
            
            if response:
                # Ajouter des conseils spécifiques au trimestre si connu
                if pregnancy_stage and pregnancy_stage in self.trimester_advice:
                    advice = self.trimester_advice[pregnancy_stage]['general']
                    response += f"\n\nℹ️ Au {pregnancy_stage.replace('_', ' ')}: {advice}"
                
                # Ajouter quand consulter
                response += "\n\n⚠️ Consultez votre médecin si les symptômes s'aggravent ou persistent."
                
                return response
        
        # Réponse générale sur les symptômes
        return ("Je comprends votre inquiétude concernant vos symptômes. "
               "Pouvez-vous me décrire plus précisément ce que vous ressentez ? "
               "Par exemple : nausées, fatigue, douleurs, etc. "
               "Cela m'aidera à vous donner des conseils plus adaptés.")
    
    def handle_general_question(self, message_analysis: Dict) -> str:
        """Traite les questions générales"""
        message = message_analysis['cleaned_message'].lower()
        
        # Vérifier la FAQ d'abord
        faq_response = message_analysis.get('faq_match')
        if faq_response:
            return faq_response
        
        # Rechercher dans la base de connaissances
        topic = self.knowledge_base.find_best_match(message)
        if topic:
            response = self.knowledge_base.get_response(topic, message)
            if response:
                return response
        
        # Questions spécifiques
        if any(word in message for word in ['combien', 'poids', 'kilos']):
            return ("Une prise de poids normale pendant la grossesse est de 9-12 kg pour un IMC normal. "
                   "Cela dépend de votre poids initial. Votre médecin vous donnera des recommandations personnalisées.")
        
        if any(word in message for word in ['quand', 'accouchement', 'naissance']):
            return ("L'accouchement a généralement lieu entre 37 et 42 semaines. "
                   "Signes du travail : contractions régulières, perte du bouchon muqueux, rupture de la poche des eaux. "
                   "Chaque grossesse est unique !")
        
        if any(word in message for word in ['manger', 'alimentation', 'nourriture']):
            return self.knowledge_base.get_response('alimentation', message)
        
        if any(word in message for word in ['sport', 'exercice', 'activité']):
            return self.knowledge_base.get_response('exercice', message)
        
        # Réponse par défaut avec suggestions
        return ("Je n'ai pas trouvé d'information spécifique sur votre question, mais je peux vous aider avec :\n\n"
               "• Symptômes de grossesse (nausées, fatigue, douleurs...)\n"
               "• Alimentation et nutrition\n"
               "• Exercice et activité physique\n"
               "• Développement du bébé\n"
               "• Préparation à l'accouchement\n"
               "• Signes d'alerte\n\n"
               "Pouvez-vous reformuler votre question ou choisir un de ces sujets ?")
    
    def handle_risk_evaluation(self, message_analysis: Dict) -> Dict:
        """Traite les demandes d'évaluation de risque"""
        extracted_info = message_analysis['extracted_info']
        
        # Vérifier si on a assez d'informations
        required_fields = ['age', 'semaines', 'poids', 'taille']
        missing_fields = [field for field in required_fields if field not in extracted_info]
        
        if missing_fields:
            questions = []
            if 'age' in missing_fields:
                questions.append("Quel âge avez-vous ?")
            if 'semaines' in missing_fields:
                questions.append("À combien de semaines de grossesse êtes-vous ?")
            if 'poids' in missing_fields:
                questions.append("Quel est votre poids actuel ?")
            if 'taille' in missing_fields:
                questions.append("Quelle est votre taille ?")
            
            return {
                'response': f"Pour évaluer votre profil de risque, j'ai besoin de quelques informations :\n\n" + 
                           "\n".join([f"• {q}" for q in questions]),
                'needs_more_info': True,
                'missing_fields': missing_fields
            }
        
        # Si on a toutes les infos, préparer pour l'évaluation IA
        return {
            'response': "J'ai toutes les informations nécessaires. Voulez-vous que j'évalue votre profil de risque ?",
            'ready_for_prediction': True,
            'extracted_info': extracted_info
        }
    
    def add_empathy_and_support(self, response: str, sentiment: str) -> str:
        """Ajoute de l'empathie et du soutien à la réponse selon le sentiment"""
        if sentiment == 'negatif':
            empathy_phrases = [
                "Je comprends votre inquiétude. ",
                "C'est normal de se poser des questions. ",
                "Votre préoccupation est légitime. ",
                "Je suis là pour vous rassurer. "
            ]
            response = random.choice(empathy_phrases) + response
            response += "\n\n💝 N'hésitez pas à me poser d'autres questions. Vous n'êtes pas seule dans cette aventure !"
        
        elif sentiment == 'positif':
            encouragement = [
                "\n\n😊 C'est merveilleux de voir votre enthousiasme !",
                "\n\n🌟 Votre attitude positive est excellente pour vous et votre bébé !",
                "\n\n💕 Continuez comme ça, vous êtes sur la bonne voie !"
            ]
            response += random.choice(encouragement)
        
        return response
    
    def process_message(self, user_message: str) -> Dict[str, any]:
        """Traite un message utilisateur et génère une réponse complète"""
        # Analyser le message avec NLP
        message_analysis = self.nlp_processor.process_message(user_message)
        
        # Mettre à jour le profil utilisateur
        self.update_user_profile(message_analysis['extracted_info'])
        
        # Ajouter à l'historique
        self.conversation_history.append({
            'user_message': user_message,
            'analysis': message_analysis,
            'timestamp': None  # À ajouter si besoin
        })
        
        # Traiter selon l'intention
        intention = message_analysis['intention']
        response_data = {'needs_more_info': False, 'ready_for_prediction': False}
        
        # Priorité absolue aux urgences
        if message_analysis['is_emergency'] or intention == 'urgence':
            response = self.handle_emergency(message_analysis)
        
        elif intention == 'salutation':
            response = self.get_personalized_greeting()
        
        elif intention in ['remerciement', 'au_revoir']:
            response = random.choice(self.default_responses[intention])
        
        elif intention == 'symptome':
            response = self.handle_symptom_inquiry(message_analysis)
        
        elif intention == 'evaluation_risque':
            eval_result = self.handle_risk_evaluation(message_analysis)
            response = eval_result['response']
            response_data.update(eval_result)
        
        else:  # question_generale ou autres
            response = self.handle_general_question(message_analysis)
        
        # Ajouter empathie et soutien
        response = self.add_empathy_and_support(response, message_analysis['sentiment'])
        
        # Ajouter des questions de suivi si pertinentes
        if message_analysis['follow_up_questions'] and not message_analysis['is_emergency']:
            response += "\n\n" + "\n".join([f"❓ {q}" for q in message_analysis['follow_up_questions'][:2]])
        
        return {
            'response': response,
            'intention': intention,
            'sentiment': message_analysis['sentiment'],
            'is_emergency': message_analysis['is_emergency'],
            'user_profile': self.user_profile.copy(),
            **response_data
        }
    
    def get_conversation_summary(self) -> str:
        """Génère un résumé de la conversation"""
        if not self.conversation_history:
            return "Aucune conversation en cours."
        
        intentions = [msg['analysis']['intention'] for msg in self.conversation_history]
        most_common = max(set(intentions), key=intentions.count)
        
        summary = f"Conversation focalisée sur : {most_common}\n"
        summary += f"Profil utilisateur : {self.user_profile}\n"
        summary += f"Nombre de messages : {len(self.conversation_history)}"
        
        return summary
    
    def reset_conversation(self):
        """Remet à zéro la conversation"""
        self.conversation_history = []
        self.user_profile = {}
    
    def get_health_tips(self) -> str:
        """Retourne des conseils de santé aléatoires"""
        tips = [
            "💧 N'oubliez pas de boire 1,5-2L d'eau par jour !",
            "🚶‍♀️ Une marche de 30 minutes par jour est excellente pendant la grossesse.",
            "🥬 Mangez 5 fruits et légumes par jour pour les vitamines.",
            "😴 Dormez sur le côté gauche pour améliorer la circulation.",
            "🧘‍♀️ Pratiquez la relaxation pour gérer le stress.",
            "📱 Téléchargez une app pour suivre le développement de bébé !",
            "👥 Rejoignez un cours de préparation à l'accouchement.",
            "📋 Tenez un carnet de grossesse pour noter vos questions."
        ]
        
        return random.choice(tips)
