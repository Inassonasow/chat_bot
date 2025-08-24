"""
Base de connaissances pour le chatbot de grossesse
Contient toutes les informations sur la grossesse, les symptômes, les conseils, etc.
"""

import re
from typing import Dict, List, Tuple, Optional
from difflib import get_close_matches

class GrossesseKnowledgeBase:
    """Base de connaissances complète sur la grossesse"""
    
    def __init__(self):
        self.knowledge = {
            # Informations générales sur la grossesse
            "grossesse_generale": {
                "durée": "Une grossesse dure environ 9 mois (40 semaines) à partir de la dernière menstruation.",
                "trimestres": "La grossesse est divisée en 3 trimestres : 1er (0-12 semaines), 2ème (13-28 semaines), 3ème (29-40 semaines).",
                "développement": "Le bébé se développe progressivement : formation des organes au 1er trimestre, croissance au 2ème, maturation au 3ème.",
                "suivi": "Un suivi médical régulier est essentiel avec des consultations mensuelles puis plus fréquentes."
            },
            
            # Symptômes par trimestre
            "symptomes": {
                "premier_trimestre": {
                    "nausées": "Les nausées matinales touchent 70% des femmes enceintes. Elles disparaissent généralement vers 12-14 semaines.",
                    "fatigue": "La fatigue est normale au 1er trimestre due aux changements hormonaux. Reposez-vous davantage.",
                    "seins_tendus": "Les seins peuvent devenir sensibles et plus volumineux dès les premières semaines.",
                    "fréquence_urinaire": "Le besoin d'uriner plus souvent est normal, l'utérus appuie sur la vessie."
                },
                "deuxieme_trimestre": {
                    "mouvements_bebe": "Vous devriez sentir les premiers mouvements entre 18-22 semaines.",
                    "douleurs_ligaments": "Des douleurs dans le bas-ventre peuvent survenir lors de l'étirement des ligaments.",
                    "reflux": "Les brûlures d'estomac peuvent commencer à cause de la pression sur l'estomac."
                },
                "troisieme_trimestre": {
                    "essoufflement": "L'essoufflement est normal, le bébé appuie sur le diaphragme.",
                    "jambes_lourdes": "Les jambes lourdes et gonflées sont fréquentes. Surélevez vos jambes.",
                    "contractions_braxton": "Les contractions de Braxton-Hicks (fausses contractions) préparent l'utérus.",
                    "insomnie": "Les troubles du sommeil sont courants. Utilisez des coussins pour vous soutenir."
                }
            },
            
            # Alimentation pendant la grossesse
            "alimentation": {
                "aliments_conseilles": [
                    "Fruits et légumes frais (5 portions par jour)",
                    "Protéines : viandes bien cuites, poissons, œufs, légumineuses",
                    "Produits laitiers : lait, yaourts, fromages pasteurisés",
                    "Céréales complètes et féculents",
                    "Eau (1,5-2L par jour)"
                ],
                "aliments_eviter": [
                    "Viandes crues ou peu cuites (tartare, carpaccio)",
                    "Poissons crus (sushi, sashimi)",
                    "Fromages au lait cru (roquefort, camembert)",
                    "Alcool (strictement interdit)",
                    "Café (limiter à 1-2 tasses/jour)",
                    "Œufs crus ou peu cuits"
                ],
                "supplements": {
                    "acide_folique": "400μg par jour avant la conception et pendant le 1er trimestre pour prévenir les malformations.",
                    "fer": "Souvent prescrit en cas d'anémie, surtout au 2ème et 3ème trimestre.",
                    "vitamine_d": "Importante pour le développement osseux du bébé.",
                    "calcium": "1000mg par jour pour la formation des os et dents du bébé."
                }
            },
            
            # Exercice et activité physique
            "exercice": {
                "recommandations": "30 minutes d'exercice modéré par jour sont recommandées sauf contre-indication médicale.",
                "activites_conseillees": [
                    "Marche",
                    "Natation",
                    "Yoga prénatal",
                    "Pilates adapté",
                    "Vélo stationnaire"
                ],
                "activites_eviter": [
                    "Sports de contact",
                    "Équitation",
                    "Ski alpin",
                    "Plongée sous-marine",
                    "Sports à risque de chute"
                ]
            },
            
            # Signes d'alerte
            "signes_alerte": {
                "urgences": [
                    "Saignements vaginaux abondants",
                    "Douleurs abdominales intenses",
                    "Contractions régulières avant 37 semaines",
                    "Perte de liquide amniotique",
                    "Maux de tête sévères avec vision trouble",
                    "Vomissements persistants empêchant l'alimentation"
                ],
                "consultation_rapide": [
                    "Fièvre supérieure à 38°C",
                    "Brûlures en urinant",
                    "Diminution des mouvements fœtaux",
                    "Gonflement soudain des mains et visage",
                    "Douleurs pelviennes persistantes"
                ]
            },
            
            # Préparation à l'accouchement
            "accouchement": {
                "signes_travail": [
                    "Contractions régulières et douloureuses",
                    "Perte du bouchon muqueux",
                    "Rupture de la poche des eaux",
                    "Douleurs dans le bas du dos"
                ],
                "preparation": "Les cours de préparation à l'accouchement aident à comprendre le processus et gérer la douleur.",
                "valise_maternite": [
                    "Documents (carte vitale, dossier médical)",
                    "Vêtements pour maman et bébé",
                    "Articles de toilette",
                    "Serviettes hygiéniques post-partum"
                ]
            },
            
            # Bien-être et conseils
            "bien_etre": {
                "sommeil": "Dormez sur le côté gauche pour améliorer la circulation. Utilisez des coussins de grossesse.",
                "stress": "Pratiquez la relaxation, la méditation ou le yoga pour gérer le stress.",
                "travail": "Vous avez droit à des pauses et aménagements. Le congé maternité commence 6 semaines avant l'accouchement.",
                "voyage": "Les voyages sont possibles jusqu'au 7ème mois, privilégiez le train ou la voiture avec pauses."
            },
            
            # Examens médicaux
            "examens": {
                "echographies": "3 échographies obligatoires : 12SA, 22SA, 32SA pour surveiller le développement.",
                "prises_sang": "Surveillance de l'anémie, diabète gestationnel, infections.",
                "monitoring": "Surveillance du rythme cardiaque fœtal en fin de grossesse."
            }
        }
        
        # Mots-clés pour l'identification des sujets
        self.keywords = {
            "nausées": ["nausée", "nausées", "vomissement", "vomissements", "mal au cœur", "envie de vomir"],
            "fatigue": ["fatigue", "fatiguée", "épuisée", "sommeil", "dormir", "énergique"],
            "alimentation": ["manger", "aliment", "nourriture", "régime", "nutrition", "vitamines"],
            "exercice": ["sport", "exercice", "activité", "bouger", "marche", "natation"],
            "douleur": ["douleur", "mal", "souffrance", "contractions", "crampes"],
            "bébé": ["bébé", "fœtus", "enfant", "mouvements", "bouger"],
            "accouchement": ["accouchement", "naissance", "travail", "contractions", "maternité"],
            "symptômes": ["symptôme", "signe", "problème", "inquiétude", "normal"]
        }
    
    def find_best_match(self, user_input: str) -> Optional[str]:
        """Trouve la meilleure correspondance dans la base de connaissances"""
        user_input = user_input.lower()
        
        # Recherche par mots-clés
        for topic, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in user_input:
                    return topic
        
        # Recherche approximative
        all_topics = list(self.keywords.keys())
        matches = get_close_matches(user_input, all_topics, n=1, cutoff=0.6)
        if matches:
            return matches[0]
        
        return None
    
    def get_response(self, topic: str, user_input: str = "") -> str:
        """Génère une réponse basée sur le sujet identifié"""
        user_input = user_input.lower()
        
        if topic == "nausées":
            return ("Les nausées sont très courantes pendant la grossesse, surtout au 1er trimestre. "
                   "Voici quelques conseils : mangez de petits repas fréquents, évitez les odeurs fortes, "
                   "buvez du thé au gingembre, et reposez-vous. Si les vomissements sont très fréquents, "
                   "consultez votre médecin.")
        
        elif topic == "fatigue":
            return ("La fatigue est normale pendant la grossesse, surtout au 1er et 3ème trimestre. "
                   "Conseils : dormez 8-9h par nuit, faites des siestes si possible, mangez équilibré, "
                   "et pratiquez une activité physique douce. N'hésitez pas à demander de l'aide.")
        
        elif topic == "alimentation":
            if "éviter" in user_input or "interdite" in user_input:
                return ("Aliments à éviter : viandes crues, poissons crus, fromages au lait cru, "
                       "alcool (strictement interdit), œufs crus, et limiter le café. "
                       "Privilégiez les aliments bien cuits et les produits pasteurisés.")
            else:
                return ("Une alimentation équilibrée est essentielle : 5 fruits et légumes par jour, "
                       "protéines (viandes cuites, poissons, œufs), produits laitiers pasteurisés, "
                       "céréales complètes. Prenez de l'acide folique et buvez 1,5-2L d'eau par jour.")
        
        elif topic == "exercice":
            return ("L'exercice est bénéfique pendant la grossesse : marche, natation, yoga prénatal. "
                   "Évitez les sports de contact et à risque de chute. 30 minutes d'activité modérée "
                   "par jour sont recommandées, sauf contre-indication médicale.")
        
        elif topic == "douleur":
            if "ventre" in user_input or "abdomen" in user_input:
                return ("Les douleurs abdominales peuvent être normales (étirement des ligaments) "
                       "ou nécessiter une consultation. Si les douleurs sont intenses, persistantes "
                       "ou accompagnées de saignements, consultez rapidement.")
            else:
                return ("Différents types de douleurs peuvent survenir pendant la grossesse. "
                       "La plupart sont normales mais certaines nécessitent une consultation. "
                       "Décrivez-moi plus précisément votre douleur pour vous aider davantage.")
        
        elif topic == "bébé":
            if "mouvement" in user_input or "bouger" in user_input:
                return ("Les premiers mouvements se sentent entre 18-22 semaines. Au 3ème trimestre, "
                       "comptez les mouvements : au moins 10 mouvements en 2 heures. Si vous notez "
                       "une diminution, consultez rapidement.")
            else:
                return ("Le développement du bébé se fait progressivement : formation des organes "
                       "au 1er trimestre, croissance rapide au 2ème, maturation au 3ème. "
                       "Les échographies permettent de suivre son développement.")
        
        elif topic == "accouchement":
            return ("Signes du travail : contractions régulières et douloureuses, perte du bouchon "
                   "muqueux, rupture de la poche des eaux. Les cours de préparation vous aideront "
                   "à mieux comprendre le processus et gérer la douleur.")
        
        elif topic == "symptômes":
            return ("De nombreux symptômes sont normaux pendant la grossesse : nausées, fatigue, "
                   "seins tendus, fréquence urinaire... Cependant, certains signes nécessitent "
                   "une consultation : saignements, douleurs intenses, fièvre, maux de tête sévères.")
        
        return None
    
    def get_general_info(self, category: str) -> str:
        """Retourne des informations générales sur une catégorie"""
        if category in self.knowledge:
            info = self.knowledge[category]
            if isinstance(info, dict):
                return " ".join([f"{key}: {value}" for key, value in info.items()])
            return str(info)
        return None
    
    def search_symptoms(self, symptom: str) -> List[str]:
        """Recherche des informations sur un symptôme spécifique"""
        results = []
        symptom = symptom.lower()
        
        for trimester, symptoms in self.knowledge["symptomes"].items():
            for symp_name, description in symptoms.items():
                if symptom in symp_name.lower() or symptom in description.lower():
                    results.append(f"{symp_name.replace('_', ' ').title()}: {description}")
        
        return results
    
    def get_emergency_info(self) -> str:
        """Retourne les informations sur les signes d'urgence"""
        urgences = self.knowledge["signes_alerte"]["urgences"]
        consultation = self.knowledge["signes_alerte"]["consultation_rapide"]
        
        return (f"🚨 SIGNES D'URGENCE (appelez immédiatement) : "
               f"{', '.join(urgences[:3])}... "
               f"⚠️ CONSULTATION RAPIDE : {', '.join(consultation[:3])}...")
