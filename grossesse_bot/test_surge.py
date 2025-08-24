"""
Script de test pour l'application Surge
Vérifie que tous les fichiers sont créés correctement
"""

import os
import json
from pathlib import Path

def test_surge_app():
    """Teste la création de l'application Surge"""
    
    print("🧪 Test de l'application Surge")
    print("=" * 40)
    
    # Vérifier que surge_app.py existe
    if not os.path.exists("surge_app.py"):
        print("❌ surge_app.py non trouvé")
        return False
    
    # Créer l'application
    print("📁 Création de l'application...")
    os.system("python surge_app.py")
    
    # Vérifier que le dossier surge_build existe
    build_dir = Path("surge_build")
    if not build_dir.exists():
        print("❌ Dossier surge_build non créé")
        return False
    
    print("✅ Dossier surge_build créé")
    
    # Vérifier les fichiers requis
    required_files = [
        "index.html",
        "styles.css", 
        "app.js",
        "surge.json",
        "README_SURGE.md"
    ]
    
    missing_files = []
    for file in required_files:
        file_path = build_dir / file
        if file_path.exists():
            print(f"✅ {file} - OK")
        else:
            print(f"❌ {file} - MANQUANT")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Fichiers manquants : {', '.join(missing_files)}")
        return False
    
    # Vérifier le contenu des fichiers
    print("\n🔍 Vérification du contenu...")
    
    # Vérifier index.html
    with open(build_dir / "index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
        if "🤰 Assistant Grossesse IA" in html_content:
            print("✅ index.html - Contenu correct")
        else:
            print("❌ index.html - Contenu incorrect")
            return False
    
    # Vérifier styles.css
    with open(build_dir / "styles.css", "r", encoding="utf-8") as f:
        css_content = f.read()
        if ":root" in css_content and "--primary-color" in css_content:
            print("✅ styles.css - Contenu correct")
        else:
            print("❌ styles.css - Contenu incorrect")
            return False
    
    # Vérifier app.js
    with open(build_dir / "app.js", "r", encoding="utf-8") as f:
        js_content = f.read()
        if "class GrossesseAssistant" in js_content:
            print("✅ app.js - Contenu correct")
        else:
            print("❌ app.js - Contenu incorrect")
            return False
    
    # Vérifier surge.json
    try:
        with open(build_dir / "surge.json", "r", encoding="utf-8") as f:
            surge_config = json.load(f)
            if "project" in surge_config and "domain" in surge_config:
                print("✅ surge.json - Configuration correcte")
            else:
                print("❌ surge.json - Configuration incorrecte")
                return False
    except Exception as e:
        print(f"❌ surge.json - Erreur de lecture : {e}")
        return False
    
    # Vérifier README_SURGE.md
    with open(build_dir / "README_SURGE.md", "r", encoding="utf-8") as f:
        readme_content = f.read()
        if "Déploiement Surge" in readme_content:
            print("✅ README_SURGE.md - Contenu correct")
        else:
            print("❌ README_SURGE.md - Contenu incorrect")
            return False
    
    print("\n🎉 Tous les tests sont passés avec succès !")
    print("🚀 Votre application Surge est prête pour le déploiement")
    
    return True

def test_local_preview():
    """Teste l'aperçu local de l'application"""
    
    print("\n🌐 Test de l'aperçu local...")
    
    build_dir = Path("surge_build")
    index_path = build_dir / "index.html"
    
    if index_path.exists():
        print(f"✅ Fichier index.html trouvé : {index_path.absolute()}")
        print("📱 Ouvrez ce fichier dans votre navigateur pour tester l'application")
        print("🔗 Ou utilisez un serveur local : python -m http.server 8000")
    else:
        print("❌ Fichier index.html non trouvé")

def main():
    """Fonction principale de test"""
    
    print("🤰 Test complet de l'Assistant Grossesse IA pour Surge")
    print("=" * 60)
    
    # Test de création
    if test_surge_app():
        # Test d'aperçu local
        test_local_preview()
        
        print("\n" + "=" * 60)
        print("🎯 PROCHAINES ÉTAPES :")
        print("1. Testez l'application localement en ouvrant index.html")
        print("2. Déployez sur Surge avec la commande : cd surge_build && surge")
        print("3. Partagez votre URL Surge avec vos utilisateurs")
        print("=" * 60)
    else:
        print("\n❌ Tests échoués. Vérifiez les erreurs ci-dessus.")

if __name__ == "__main__":
    main()
