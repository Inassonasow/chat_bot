#!/usr/bin/env python
"""
Script de test pour le nouveau chatbot intelligent
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grossesse_bot.settings')
django.setup()

from chatbot.intelligent_chatbot import IntelligentGrossesseChatbot

def test_chatbot_responses():
    """Teste différents types de messages avec le chatbot"""
    
    print("🚀 TEST DU CHATBOT INTELLIGENT")
    print("=" * 50)
    
    # Créer une instance du chatbot
    chatbot = IntelligentGrossesseChatbot()
    
    # Messages de test
    test_messages = [
        "Bonjour !",
        "J'ai des nausées depuis ce matin, est-ce normal ?",
        "Je suis à 20 semaines de grossesse, j'ai 28 ans, je pèse 65 kg et je mesure 165 cm",
        "Qu'est-ce que je peux manger pendant ma grossesse ?",
        "J'ai mal au ventre, c'est grave ?",
        "Quand vais-je accoucher ?",
        "Puis-je faire du sport ?",
        "J'ai des saignements abondants",  # Test d'urgence
        "Merci pour vos conseils",
        "Au revoir"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🔍 Test {i}/10")
        print(f"👤 Utilisateur : {message}")
        
        try:
            # Traiter le message
            response = chatbot.process_message(message)
            
            print(f"🤖 Réponse : {response['response']}")
            print(f"📊 Intention : {response['intention']}")
            print(f"💭 Sentiment : {response['sentiment']}")
            
            if response['is_emergency']:
                print("🚨 URGENCE DÉTECTÉE !")
            
            if response.get('user_profile'):
                print(f"👤 Profil : {response['user_profile']}")
                
        except Exception as e:
            print(f"❌ Erreur : {str(e)}")
        
        print("-" * 50)
    
    print("\n📊 RÉSUMÉ DE LA CONVERSATION")
    print(chatbot.get_conversation_summary())

def test_knowledge_base():
    """Teste la base de connaissances"""
    print("\n🧠 TEST DE LA BASE DE CONNAISSANCES")
    print("=" * 50)
    
    from chatbot.knowledge_base import GrossesseKnowledgeBase
    
    kb = GrossesseKnowledgeBase()
    
    # Test de recherche
    topics = ['nausées', 'fatigue', 'alimentation', 'exercice']
    
    for topic in topics:
        print(f"\n📚 Sujet : {topic}")
        response = kb.get_response(topic, f"j'ai des {topic}")
        if response:
            print(f"💡 Réponse : {response[:100]}...")
        else:
            print("❌ Aucune réponse trouvée")

def test_nlp_processor():
    """Teste le processeur NLP"""
    print("\n🔤 TEST DU PROCESSEUR NLP")
    print("=" * 50)
    
    from chatbot.nlp_processor import NLPProcessor
    
    nlp = NLPProcessor()
    
    test_texts = [
        "J'ai 25 ans et je suis à 20 semaines de grossesse",
        "J'ai des nausées terribles",
        "Est-ce que je peux manger du sushi ?",
        "J'ai des saignements abondants, c'est urgent !"
    ]
    
    for text in test_texts:
        print(f"\n📝 Texte : {text}")
        analysis = nlp.process_message(text)
        
        print(f"🎯 Intention : {analysis['intention']}")
        print(f"💭 Sentiment : {analysis['sentiment']}")
        print(f"📊 Infos extraites : {analysis['extracted_info']}")
        print(f"🏥 Infos médicales : {analysis['medical_info']}")
        
        if analysis['is_emergency']:
            print("🚨 URGENCE DÉTECTÉE !")

def main():
    """Fonction principale de test"""
    try:
        test_chatbot_responses()
        test_knowledge_base()
        test_nlp_processor()
        
        print("\n" + "=" * 50)
        print("🎉 TOUS LES TESTS SONT TERMINÉS !")
        print("Le chatbot intelligent est prêt à être utilisé.")
        print("\nPour tester l'interface web :")
        print("1. Lancez : python manage.py runserver")
        print("2. Allez sur : http://127.0.0.1:8000/chatbot/")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests : {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


