#!/usr/bin/env python
"""
Script de test pour verifier l'installation du projet Chatbot Grossesse
"""

import sys
import os

def test_imports():
    """Teste l'import des packages essentiels"""
    print("🔍 Test des imports...")
    
    try:
        import django
        print(f"✅ Django {django.get_version()} - OK")
    except ImportError as e:
        print(f"❌ Django - ERREUR: {e}")
        return False
    
    try:
        import djangorestframework
        print("✅ Django REST Framework - OK")
    except ImportError as e:
        print(f"❌ Django REST Framework - ERREUR: {e}")
        return False
    
    try:
        import sklearn
        print(f"✅ Scikit-learn {sklearn.__version__} - OK")
    except ImportError as e:
        print(f"❌ Scikit-learn - ERREUR: {e}")
        return False
    
    try:
        import joblib
        print(f"✅ Joblib {joblib.__version__} - OK")
    except ImportError as e:
        print(f"❌ Joblib - ERREUR: {e}")
        return False
    
    try:
        import pandas
        print(f"✅ Pandas {pandas.__version__} - OK")
    except ImportError as e:
        print(f"❌ Pandas - ERREUR: {e}")
        return False
    
    try:
        import numpy
        print(f"✅ NumPy {numpy.__version__} - OK")
    except ImportError as e:
        print(f"❌ NumPy - ERREUR: {e}")
        return False
    
    return True

def test_files():
    """Teste l'existence des fichiers essentiels"""
    print("\n📁 Test des fichiers...")
    
    required_files = [
        "model_risque_grossesse.pkl",
        "label_encoders.pkl",
        "donnees_grossesse.csv",
        "manage.py",
        "requirements.txt"
    ]
    
    all_files_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - OK")
        else:
            print(f"❌ {file} - MANQUANT")
            all_files_exist = False
    
    return all_files_exist

def test_django_setup():
    """Teste la configuration Django"""
    print("\n🐍 Test de Django...")
    
    try:
        # Configuration Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grossesse_bot.settings')
        
        import django
        django.setup()
        
        print("✅ Configuration Django - OK")
        
        # Test des modèles
        from chatbot.models import EvaluationGrossesse
        print("✅ Modèles Django - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration Django - ERREUR: {e}")
        return False

def test_model():
    """Teste le chargement du modèle IA"""
    print("\n🤖 Test du modèle IA...")
    
    try:
        import joblib
        import numpy as np
        
        # Charger le modèle
        model = joblib.load('model_risque_grossesse.pkl')
        print("✅ Modèle chargé - OK")
        
        # Test de prédiction
        test_input = [30, 6, 70.0, 165.0, 1, 0, 1, 0]  # Exemple de test
        prediction = model.predict([test_input])[0]
        print(f"✅ Prédiction test: {prediction} - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Modèle IA - ERREUR: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST D'INSTALLATION - CHATBOT GROSSESSE")
    print("=" * 50)
    
    # Tests
    imports_ok = test_imports()
    files_ok = test_files()
    django_ok = test_django_setup()
    model_ok = test_model()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    tests = [
        ("Imports", imports_ok),
        ("Fichiers", files_ok),
        ("Django", django_ok),
        ("Modèle IA", model_ok)
    ]
    
    all_passed = True
    for test_name, passed in tests:
        status = "✅ PASSÉ" if passed else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 TOUS LES TESTS SONT PASSÉS !")
        print("Votre projet est prêt à être utilisé.")
        print("\nPour démarrer le serveur:")
        print("python manage.py runserver")
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez l'installation et réessayez.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()


