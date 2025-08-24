"""
Processeur de langage naturel pour le chatbot de grossesse
Analyse les messages des utilisateurs et extrait les intentions
"""

import re
from typing import Dict, List, Tuple, Optional
from difflib import get_close_matches

class NLPProcessor:
    """Processeur de langage naturel pour comprendre les questions des utilisateurs"""
    
    def __init__(self):
        # Patterns pour extraire des informations
        self.patterns = {
            'age': r'(\d+)\s*ans?',
            'semaines': r'(\d+)\s*semaines?',
            'mois': r'(\d+)\s*mois',
            'poids': r'(\d+(?:\.\d+)?)\s*kg',
            'taille': r'(\d+)\s*cm',
            'temperature': r'(\d+(?:\.\d+)?)\s*°?[Cc]?',
        }
        
        # Intentions possibles
        self.intentions = {
            'salutation': [
                'bonjour', 'bonsoir', 'salut', 'hello', 'coucou', 'hey'
            ],
            'remerciement': [
                'merci', 'merci beaucoup', 'thanks', 'thank you'
            ],
            'au_revoir': [
                'au revoir', 'bye', 'à bientôt', 'salut', 'tchao'
            ],
            'question_generale': [
                'qu\'est-ce que', 'c\'est quoi', 'comment', 'pourquoi', 'quand',
                'où', 'qui', 'que', 'quel', 'quelle', 'combien'
            ],
            'demande_aide': [
                'aide', 'aider', 'help', 'problème', 'souci', 'inquiète', 'inquiet'
            ],
            'symptome': [
                'j\'ai mal', 'je ressens', 'je sens', 'douleur', 'symptôme',
                'problème', 'inquiète', 'normal'
            ],
            'conseil': [
                'conseil', 'que faire', 'recommandation', 'suggestion'
            ],
            'evaluation_risque': [
                'risque', 'évaluation', 'analyser', 'prédire', 'diagnostic'
            ]
        }
        
        # Questions fréquentes et leurs réponses
        self.faq = {
            'enceinte': "Si vous pensez être enceinte, faites un test de grossesse et consultez un médecin pour confirmer.",
            'test grossesse': "Les tests de grossesse sont fiables dès le premier jour de retard des règles.",
            'premier rdv': "Le premier rendez-vous se fait généralement vers 6-8 semaines de grossesse.",
            'échographie': "3 échographies sont obligatoires : 12SA, 22SA et 32SA.",
            'congé maternité': "Le congé maternité commence 6 semaines avant la date prévue d'accouchement.",
            'poids grossesse': "Une prise de poids de 9-12 kg est normale pendant la grossesse.",
            'alcool': "L'alcool est strictement interdit pendant toute la grossesse.",
            'café': "Limitez le café à 1-2 tasses par jour maximum.",
            'voyage': "Les voyages sont possibles jusqu'au 7ème mois, privilégiez le train.",
            'travail': "Vous pouvez généralement travailler jusqu'au congé maternité sauf contre-indication."
        }
        
        # Expressions d'urgence
        self.urgence_keywords = [
            'saignement', 'saigne', 'sang', 'hémorragie', 'saignements',
            'douleur intense', 'très mal', 'insupportable', 'mal au ventre',
            'contractions', 'travail', 'accoucher', 'accouchement',
            'fièvre', 'température', 'chaud', 'frissons',
            'vision floue', 'mal de tête', 'migraine', 'maux de tête',
            'vomissements', 'ne peux plus manger', 'vomir',
            'perte des eaux', 'liquide', 'urgent', 'urgence', 'grave'
        ]
        
        # Mots positifs et négatifs pour l'analyse de sentiment
        self.sentiment_words = {
            'positif': [
                'bien', 'bon', 'bonne', 'super', 'génial', 'parfait',
                'heureux', 'heureuse', 'content', 'contente', 'joie'
            ],
            'negatif': [
                'mal', 'mauvais', 'terrible', 'horrible', 'inquiet',
                'inquiète', 'peur', 'stress', 'angoisse', 'problème'
            ]
        }
    
    def extract_info(self, text: str) -> Dict[str, any]:
        """Extrait les informations numériques du texte"""
        info = {}
        text = text.lower()
        
        for key, pattern in self.patterns.items():
            match = re.search(pattern, text)
            if match:
                value = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))
                info[key] = value
        
        return info
    
    def detect_intention(self, text: str) -> str:
        """Détecte l'intention principale du message"""
        text = text.lower()
        
        # Vérifier les urgences en premier
        for keyword in self.urgence_keywords:
            if keyword in text:
                return 'urgence'
        
        # Vérifier les intentions
        for intention, keywords in self.intentions.items():
            for keyword in keywords:
                if keyword in text:
                    return intention
        
        # Par défaut, c'est une question générale
        return 'question_generale'
    
    def analyze_sentiment(self, text: str) -> str:
        """Analyse le sentiment du message"""
        text = text.lower()
        
        positive_count = sum(1 for word in self.sentiment_words['positif'] if word in text)
        negative_count = sum(1 for word in self.sentiment_words['negatif'] if word in text)
        
        if negative_count > positive_count:
            return 'negatif'
        elif positive_count > negative_count:
            return 'positif'
        else:
            return 'neutre'
    
    def find_faq_match(self, text: str) -> Optional[str]:
        """Trouve une correspondance dans la FAQ"""
        text = text.lower()
        
        # Recherche exacte
        for question, answer in self.faq.items():
            if question in text:
                return answer
        
        # Recherche approximative
        questions = list(self.faq.keys())
        matches = get_close_matches(text, questions, n=1, cutoff=0.6)
        if matches:
            return self.faq[matches[0]]
        
        return None
    
    def extract_medical_info(self, text: str) -> Dict[str, str]:
        """Extrait les informations médicales du texte"""
        info = {}
        text = text.lower()
        
        # Symptômes courants
        symptoms = {
            'nausées': ['nausée', 'nausées', 'envie de vomir', 'mal au cœur'],
            'fatigue': ['fatigue', 'fatiguée', 'épuisée', 'crevée'],
            'douleurs': ['douleur', 'mal', 'souffre', 'fait mal'],
            'saignements': ['saignement', 'saigne', 'sang', 'pertes'],
            'contractions': ['contraction', 'contractions', 'ventre dur'],
            'fièvre': ['fièvre', 'température', 'chaud', 'frissons']
        }
        
        for symptom, keywords in symptoms.items():
            for keyword in keywords:
                if keyword in text:
                    info['symptome'] = symptom
                    break
        
        # Localisation de la douleur
        locations = {
            'ventre': ['ventre', 'abdomen', 'estomac'],
            'dos': ['dos', 'reins', 'lombaire'],
            'tête': ['tête', 'crâne', 'migraine'],
            'seins': ['seins', 'poitrine'],
            'jambes': ['jambes', 'pieds', 'chevilles']
        }
        
        for location, keywords in locations.items():
            for keyword in keywords:
                if keyword in text:
                    info['localisation'] = location
                    break
        
        return info
    
    def is_emergency(self, text: str) -> bool:
        """Détermine si le message indique une urgence"""
        text = text.lower()
        
        emergency_phrases = [
            'saignement abondant', 'beaucoup de sang',
            'douleur insupportable', 'très mal',
            'contractions régulières', 'travail',
            'perte des eaux', 'liquide',
            'fièvre élevée', 'plus de 38',
            'vision floue', 'maux de tête sévères',
            'vomissements incessants'
        ]
        
        for phrase in emergency_phrases:
            if phrase in text:
                return True
        
        return False
    
    def extract_pregnancy_stage(self, text: str) -> Optional[str]:
        """Détermine le stade de grossesse mentionné"""
        text = text.lower()
        
        if 'trimestre' in text:
            if 'premier' in text or '1er' in text or '1' in text:
                return 'premier_trimestre'
            elif 'deuxième' in text or '2ème' in text or '2' in text:
                return 'deuxieme_trimestre'
            elif 'troisième' in text or '3ème' in text or '3' in text:
                return 'troisieme_trimestre'
        
        # Extraction par semaines
        info = self.extract_info(text)
        if 'semaines' in info:
            weeks = info['semaines']
            if weeks <= 12:
                return 'premier_trimestre'
            elif weeks <= 28:
                return 'deuxieme_trimestre'
            else:
                return 'troisieme_trimestre'
        
        return None
    
    def generate_follow_up_questions(self, intention: str, info: Dict) -> List[str]:
        """Génère des questions de suivi basées sur l'intention et les infos"""
        questions = []
        
        if intention == 'symptome':
            if 'symptome' not in info:
                questions.append("Pouvez-vous me décrire plus précisément ce que vous ressentez ?")
            if 'localisation' not in info:
                questions.append("Où ressentez-vous cette gêne exactement ?")
            if 'age' not in info and 'semaines' not in info:
                questions.append("À quel stade de votre grossesse êtes-vous ?")
        
        elif intention == 'evaluation_risque':
            missing_info = []
            required_fields = ['age', 'semaines', 'poids', 'taille']
            
            for field in required_fields:
                if field not in info:
                    missing_info.append(field)
            
            if missing_info:
                questions.append(f"Pour une évaluation précise, j'aurais besoin de connaître : {', '.join(missing_info)}")
        
        return questions
    
    def clean_text(self, text: str) -> str:
        """Nettoie et normalise le texte"""
        # Supprimer les caractères spéciaux
        text = re.sub(r'[^\w\s\.\?\!\,\']', '', text)
        
        # Normaliser les espaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def process_message(self, message: str) -> Dict[str, any]:
        """Traite complètement un message et retourne toutes les informations extraites"""
        cleaned_message = self.clean_text(message)
        
        result = {
            'original_message': message,
            'cleaned_message': cleaned_message,
            'intention': self.detect_intention(cleaned_message),
            'sentiment': self.analyze_sentiment(cleaned_message),
            'extracted_info': self.extract_info(cleaned_message),
            'medical_info': self.extract_medical_info(cleaned_message),
            'pregnancy_stage': self.extract_pregnancy_stage(cleaned_message),
            'is_emergency': self.is_emergency(cleaned_message),
            'faq_match': self.find_faq_match(cleaned_message),
            'follow_up_questions': []
        }
        
        # Générer des questions de suivi
        result['follow_up_questions'] = self.generate_follow_up_questions(
            result['intention'], 
            {**result['extracted_info'], **result['medical_info']}
        )
        
        return result
