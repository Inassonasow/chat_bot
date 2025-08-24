"""
Configuration pour l'application Surge
Personnalisez ces paramètres selon vos besoins
"""

# Configuration de l'application
APP_CONFIG = {
    "title": "🤰 Assistant Grossesse IA",
    "subtitle": "Votre compagnon intelligent pour une grossesse sereine",
    "version": "1.0.0",
    "author": "Votre Nom",
    "description": "Assistant IA pour l'accompagnement des femmes enceintes"
}

# Configuration des couleurs
COLORS = {
    "primary": "#667eea",      # Bleu principal
    "secondary": "#764ba2",    # Violet secondaire
    "accent": "#f093fb",       # Rose accent
    "success": "#4ade80",      # Vert succès
    "warning": "#fbbf24",      # Orange avertissement
    "error": "#f87171",        # Rouge erreur
    "text_primary": "#1f2937", # Texte principal
    "text_secondary": "#6b7280" # Texte secondaire
}

# Configuration du chatbot
CHATBOT_CONFIG = {
    "welcome_message": "👋 Bonjour ! Je suis votre assistant grossesse IA. Posez-moi vos questions sur la grossesse, la nutrition, les symptômes, etc.",
    "responses": {
        "nausée": "Les nausées sont très courantes au premier trimestre. Essayez de manger de petites quantités fréquemment, évitez les odeurs fortes, et privilégiez les aliments secs comme les crackers. Si elles persistent, parlez-en à votre médecin.",
        "fatigue": "La fatigue est normale pendant la grossesse, surtout au premier et troisième trimestre. Reposez-vous quand vous le pouvez, faites des siestes courtes, et maintenez une activité physique modérée.",
        "douleur": "Toute douleur inhabituelle doit être évaluée par un professionnel de santé. Ne prenez pas d'analgésiques sans avis médical.",
        "alimentation": "Une alimentation équilibrée est essentielle. Privilégiez les fruits, légumes, protéines maigres, et céréales complètes. Évitez les aliments crus, l'alcool, et limitez la caféine.",
        "activité": "L'activité physique modérée est bénéfique : marche, natation, yoga prénatal. Évitez les sports de contact et les activités à risque de chute.",
        "sommeil": "Le sommeil peut être perturbé. Essayez de dormir sur le côté gauche, utilisez des oreillers de grossesse, et évitez les repas lourds le soir.",
        "stress": "La gestion du stress est importante. Pratiquez la respiration profonde, la méditation, et n'hésitez pas à demander de l'aide si nécessaire.",
        "exercice": "L'exercice modéré est excellent pour la santé. Marchez 30 minutes par jour, faites du yoga prénatal, ou de la natation. Écoutez votre corps et arrêtez si vous vous sentez fatiguée."
    },
    "default_response": "Je comprends votre préoccupation. Pour des conseils personnalisés, n'hésitez pas à me donner plus de détails sur votre situation. N'oubliez pas que je ne remplace pas l'avis médical de votre professionnel de santé."
}

# Configuration de l'évaluation des risques
RISK_ASSESSMENT_CONFIG = {
    "risk_factors": {
        "age": {
            "35+": 2,
            "40+": 3
        },
        "weight": {
            "100kg+": 1
        },
        "medical_history": {
            "hypertension": 3,
            "diabète": 3,
            "asthme": 1,
            "aucun": 0
        },
        "symptoms": {
            "douleur": 2,
            "nausée": 1,
            "fatigue": 1,
            "aucun": 0
        }
    },
    "risk_levels": {
        "low": {
            "max_score": 2,
            "message": "Risque faible. Continuez à prendre soin de vous et suivez les recommandations de votre médecin.",
            "color": "success"
        },
        "moderate": {
            "max_score": 5,
            "message": "Risque modéré. Surveillez vos symptômes et consultez régulièrement votre professionnel de santé.",
            "color": "warning"
        },
        "high": {
            "min_score": 6,
            "message": "Risque élevé. Consultation médicale recommandée dans les plus brefs délais.",
            "color": "error"
        }
    }
}

# Configuration des informations utiles
INFO_SECTIONS = [
    {
        "icon": "🍎",
        "title": "Nutrition",
        "description": "Conseils alimentaires adaptés à chaque trimestre de grossesse"
    },
    {
        "icon": "🏃‍♀️",
        "title": "Activité Physique",
        "description": "Exercices recommandés et précautions à prendre"
    },
    {
        "icon": "😴",
        "title": "Bien-être",
        "description": "Gestion du stress et amélioration du sommeil"
    },
    {
        "icon": "⚠️",
        "title": "Symptômes",
        "description": "Reconnaître les symptômes normaux et ceux qui nécessitent une consultation"
    }
]

# Configuration Surge
SURGE_CONFIG = {
    "project": "chatbot-grossesse",
    "domain": "chatbot-grossesse.surge.sh",
    "description": "Assistant Grossesse IA - Votre compagnon intelligent pour une grossesse sereine"
}

# Configuration des métadonnées
META_CONFIG = {
    "keywords": "grossesse, chatbot, IA, santé, nutrition, symptômes, conseils, femme enceinte",
    "author": "Assistant Grossesse IA",
    "robots": "index, follow",
    "viewport": "width=device-width, initial-scale=1.0"
}

# Configuration des polices
FONTS = {
    "primary": "Inter",
    "fallback": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
}

# Configuration des animations
ANIMATIONS = {
    "enabled": True,
    "duration": "0.3s",
    "easing": "ease-in-out"
}

# Configuration responsive
RESPONSIVE_CONFIG = {
    "breakpoints": {
        "mobile": 768,
        "tablet": 1024,
        "desktop": 1200
    },
    "mobile_first": True
}

if __name__ == "__main__":
    print("🔧 Configuration de l'Assistant Grossesse IA")
    print("=" * 50)
    print(f"Titre: {APP_CONFIG['title']}")
    print(f"Version: {APP_CONFIG['version']}")
    print(f"Auteur: {APP_CONFIG['author']}")
    print(f"Projet Surge: {SURGE_CONFIG['project']}")
    print(f"Domaine: {SURGE_CONFIG['domain']}")
    print("\n✅ Configuration chargée avec succès !")
