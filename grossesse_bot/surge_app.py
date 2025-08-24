"""
Application Surge pour le chatbot de grossesse
Version statique - génère des fichiers HTML/CSS/JS pour déploiement sur Surge
"""

import os
import json
import shutil
from pathlib import Path

def create_surge_app():
    """Crée l'application statique pour Surge"""
    
    # Créer le répertoire de sortie
    output_dir = Path("surge_build")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()
    
    # Créer le fichier principal index.html
    create_index_html(output_dir)
    
    # Créer le fichier CSS
    create_styles_css(output_dir)
    
    # Créer le fichier JavaScript
    create_app_js(output_dir)
    
    # Créer le fichier surge.json
    create_surge_config(output_dir)
    
    # Créer le README pour Surge
    create_surge_readme(output_dir)
    
    print("✅ Application Surge créée avec succès dans le dossier 'surge_build'")
    print("📁 Pour déployer : cd surge_build && surge")

def create_index_html(output_dir):
    """Crée le fichier HTML principal"""
    html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤰 Chatbot Grossesse - Assistant IA</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🤰 Assistant Grossesse IA</h1>
            <p>Votre compagnon intelligent pour une grossesse sereine</p>
        </header>
        
        <main class="main-content">
            <!-- Section Chatbot -->
            <section class="chatbot-section">
                <h2>💬 Chat avec l'IA</h2>
                <div class="chat-container">
                    <div class="chat-messages" id="chatMessages">
                        <div class="message bot-message">
                            <div class="message-content">
                                <p>👋 Bonjour ! Je suis votre assistant grossesse IA. Posez-moi vos questions sur la grossesse, la nutrition, les symptômes, etc.</p>
                            </div>
                        </div>
                    </div>
                    <div class="chat-input-container">
                        <input type="text" id="chatInput" placeholder="Posez votre question..." maxlength="500">
                        <button id="sendButton">📤</button>
                    </div>
                </div>
            </section>
            
            <!-- Section Prédiction de Risque -->
            <section class="prediction-section">
                <h2>🔮 Évaluation des Risques</h2>
                <form id="predictionForm" class="prediction-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="age">Âge</label>
                            <input type="number" id="age" name="age" min="15" max="50" required>
                        </div>
                        <div class="form-group">
                            <label for="mois_grossesse">Mois de grossesse</label>
                            <input type="number" id="mois_grossesse" name="mois_grossesse" min="1" max="9" required>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="poids_kg">Poids (kg)</label>
                            <input type="number" id="poids_kg" name="poids_kg" min="40" max="150" step="0.1" required>
                        </div>
                        <div class="form-group">
                            <label for="taille_cm">Taille (cm)</label>
                            <input type="number" id="taille_cm" name="taille_cm" min="140" max="200" required>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="activite">Niveau d'activité</label>
                            <select id="activite" name="activite" required>
                                <option value="">Choisir...</option>
                                <option value="faible">Faible</option>
                                <option value="modérée">Modérée</option>
                                <option value="élevée">Élevée</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="regime">Régime alimentaire</label>
                            <select id="regime" name="regime" required>
                                <option value="">Choisir...</option>
                                <option value="omnivore">Omnivore</option>
                                <option value="végétarien">Végétarien</option>
                                <option value="autre">Autre</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="antecedents">Antécédents médicaux</label>
                            <select id="antecedents" name="antecedents" required>
                                <option value="">Choisir...</option>
                                <option value="aucun">Aucun</option>
                                <option value="hypertension">Hypertension</option>
                                <option value="diabète">Diabète</option>
                                <option value="asthme">Asthme</option>
                                <option value="autre">Autre</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="symptome">Symptômes actuels</label>
                            <select id="symptome" name="symptome" required>
                                <option value="">Choisir...</option>
                                <option value="aucun">Aucun</option>
                                <option value="nausée">Nausée</option>
                                <option value="fatigue">Fatigue</option>
                                <option value="douleur">Douleur</option>
                            </select>
                        </div>
                    </div>
                    
                    <button type="submit" class="submit-btn">🔮 Évaluer les risques</button>
                </form>
                
                <div id="predictionResult" class="prediction-result hidden"></div>
            </section>
            
            <!-- Section Informations -->
            <section class="info-section">
                <h2>📚 Informations Utiles</h2>
                <div class="info-grid">
                    <div class="info-card">
                        <h3>🍎 Nutrition</h3>
                        <p>Conseils alimentaires adaptés à chaque trimestre de grossesse</p>
                    </div>
                    <div class="info-card">
                        <h3>🏃‍♀️ Activité Physique</h3>
                        <p>Exercices recommandés et précautions à prendre</p>
                    </div>
                    <div class="info-card">
                        <h3>😴 Bien-être</h3>
                        <p>Gestion du stress et amélioration du sommeil</p>
                    </div>
                    <div class="info-card">
                        <h3>⚠️ Symptômes</h3>
                        <p>Reconnaître les symptômes normaux et ceux qui nécessitent une consultation</p>
                    </div>
                </div>
            </section>
        </main>
        
        <footer class="footer">
            <p>🤰 Assistant Grossesse IA - Développé avec ❤️ pour les futures mamans</p>
            <p><small>⚠️ Cet outil ne remplace pas l'avis médical. Consultez toujours votre professionnel de santé.</small></p>
        </footer>
    </div>
    
    <script src="app.js"></script>
</body>
</html>"""
    
    with open(output_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def create_styles_css(output_dir):
    """Crée le fichier CSS"""
    css_content = """/* Styles pour l'Assistant Grossesse IA */

:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #f093fb;
    --success-color: #4ade80;
    --warning-color: #fbbf24;
    --error-color: #f87171;
    --text-primary: #1f2937;
    --text-secondary: #6b7280;
    --bg-primary: #ffffff;
    --bg-secondary: #f9fafb;
    --border-color: #e5e7eb;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.6;
    color: var(--text-primary);
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Header */
.header {
    text-align: center;
    margin-bottom: 40px;
    color: white;
}

.header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 10px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.header p {
    font-size: 1.2rem;
    opacity: 0.9;
}

/* Main Content */
.main-content {
    display: grid;
    gap: 30px;
}

/* Chatbot Section */
.chatbot-section, .prediction-section, .info-section {
    background: var(--bg-primary);
    border-radius: 16px;
    padding: 30px;
    box-shadow: var(--shadow);
}

.chatbot-section h2, .prediction-section h2, .info-section h2 {
    color: var(--primary-color);
    margin-bottom: 20px;
    font-size: 1.5rem;
    font-weight: 600;
}

/* Chat Container */
.chat-container {
    border: 2px solid var(--border-color);
    border-radius: 12px;
    overflow: hidden;
}

.chat-messages {
    height: 400px;
    overflow-y: auto;
    padding: 20px;
    background: var(--bg-secondary);
}

.message {
    margin-bottom: 15px;
    display: flex;
}

.bot-message {
    justify-content: flex-start;
}

.user-message {
    justify-content: flex-end;
}

.message-content {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 18px;
    background: var(--primary-color);
    color: white;
}

.user-message .message-content {
    background: var(--accent-color);
}

.chat-input-container {
    display: flex;
    padding: 15px;
    background: white;
    border-top: 1px solid var(--border-color);
}

#chatInput {
    flex: 1;
    padding: 12px 16px;
    border: 2px solid var(--border-color);
    border-radius: 25px;
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s;
}

#chatInput:focus {
    border-color: var(--primary-color);
}

#sendButton {
    margin-left: 10px;
    padding: 12px 16px;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: 18px;
    transition: transform 0.2s;
}

#sendButton:hover {
    transform: scale(1.1);
}

/* Prediction Form */
.prediction-form {
    display: grid;
    gap: 20px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--text-secondary);
}

.form-group input, .form-group select {
    padding: 12px 16px;
    border: 2px solid var(--border-color);
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.3s;
}

.form-group input:focus, .form-group select:focus {
    outline: none;
    border-color: var(--primary-color);
}

.submit-btn {
    padding: 16px 32px;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    border: none;
    border-radius: 25px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s;
    margin-top: 10px;
}

.submit-btn:hover {
    transform: translateY(-2px);
}

/* Prediction Result */
.prediction-result {
    margin-top: 20px;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

.prediction-result.success {
    background: var(--success-color);
    color: white;
}

.prediction-result.warning {
    background: var(--warning-color);
    color: white;
}

.prediction-result.error {
    background: var(--error-color);
    color: white;
}

.hidden {
    display: none;
}

/* Info Grid */
.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.info-card {
    padding: 20px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border-left: 4px solid var(--primary-color);
}

.info-card h3 {
    color: var(--primary-color);
    margin-bottom: 10px;
    font-weight: 600;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 40px;
    color: white;
    opacity: 0.8;
}

.footer p {
    margin-bottom: 10px;
}

/* Responsive */
@media (max-width: 768px) {
    .container {
        padding: 15px;
    }
    
    .header h1 {
        font-size: 2rem;
    }
    
    .form-row {
        grid-template-columns: 1fr;
    }
    
    .info-grid {
        grid-template-columns: 1fr;
    }
    
    .chatbot-section, .prediction-section, .info-section {
        padding: 20px;
    }
}

/* Loading Animation */
.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255,255,255,.3);
    border-radius: 50%;
    border-top-color: #fff;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}"""
    
    with open(output_dir / "styles.css", "w", encoding="utf-8") as f:
        f.write(css_content)

def create_app_js(output_dir):
    """Crée le fichier JavaScript"""
    js_content = """// Application JavaScript pour l'Assistant Grossesse IA

class GrossesseAssistant {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.loading = false;
    }
    
    initializeElements() {
        this.chatInput = document.getElementById('chatInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.predictionForm = document.getElementById('predictionForm');
        this.predictionResult = document.getElementById('predictionResult');
    }
    
    bindEvents() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
        this.predictionForm.addEventListener('submit', (e) => this.handlePrediction(e));
    }
    
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message || this.loading) return;
        
        // Ajouter le message utilisateur
        this.addMessage(message, 'user');
        this.chatInput.value = '';
        
        // Simuler la réponse de l'IA
        this.loading = true;
        this.sendButton.innerHTML = '<span class="loading"></span>';
        
        try {
            const response = await this.getChatbotResponse(message);
            this.addMessage(response, 'bot');
        } catch (error) {
            this.addMessage("Désolé, je rencontre des difficultés techniques. Veuillez réessayer.", 'bot');
        } finally {
            this.loading = false;
            this.sendButton.innerHTML = '📤';
        }
    }
    
    async getChatbotResponse(message) {
        // Simulation de réponses intelligentes
        const responses = {
            'nausée': "Les nausées sont très courantes au premier trimestre. Essayez de manger de petites quantités fréquemment, évitez les odeurs fortes, et privilégiez les aliments secs comme les crackers. Si elles persistent, parlez-en à votre médecin.",
            'fatigue': "La fatigue est normale pendant la grossesse, surtout au premier et troisième trimestre. Reposez-vous quand vous le pouvez, faites des siestes courtes, et maintenez une activité physique modérée.",
            'douleur': "Toute douleur inhabituelle doit être évaluée par un professionnel de santé. Ne prenez pas d'analgésiques sans avis médical.",
            'alimentation': "Une alimentation équilibrée est essentielle. Privilégiez les fruits, légumes, protéines maigres, et céréales complètes. Évitez les aliments crus, l'alcool, et limitez la caféine.",
            'activité': "L'activité physique modérée est bénéfique : marche, natation, yoga prénatal. Évitez les sports de contact et les activités à risque de chute.",
            'sommeil': "Le sommeil peut être perturbé. Essayez de dormir sur le côté gauche, utilisez des oreillers de grossesse, et évitez les repas lourds le soir."
        };
        
        // Recherche de mots-clés dans le message
        const lowerMessage = message.toLowerCase();
        for (const [keyword, response] of Object.entries(responses)) {
            if (lowerMessage.includes(keyword)) {
                return response;
            }
        }
        
        // Réponse par défaut
        return "Je comprends votre préoccupation. Pour des conseils personnalisés, n'hésitez pas à me donner plus de détails sur votre situation. N'oubliez pas que je ne remplace pas l'avis médical de votre professionnel de santé.";
    }
    
    addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = `<p>${content}</p>`;
        
        messageDiv.appendChild(messageContent);
        this.chatMessages.appendChild(messageDiv);
        
        // Scroll vers le bas
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    async handlePrediction(e) {
        e.preventDefault();
        
        const formData = new FormData(this.predictionForm);
        const data = {
            age: parseInt(formData.get('age')),
            mois_grossesse: parseInt(formData.get('mois_grossesse')),
            poids_kg: parseFloat(formData.get('poids_kg')),
            taille_cm: parseInt(formData.get('taille_cm')),
            activité: formData.get('activite'),
            régime: formData.get('regime'),
            antécédents: formData.get('antecedents'),
            symptôme: formData.get('symptome')
        };
        
        try {
            const result = await this.predictRisk(data);
            this.showPredictionResult(result);
        } catch (error) {
            this.showPredictionResult({
                niveau: 'error',
                message: 'Erreur lors de l\'évaluation. Veuillez réessayer.'
            });
        }
    }
    
    async predictRisk(data) {
        // Simulation de prédiction basée sur des règles simples
        let riskScore = 0;
        
        // Facteurs de risque
        if (data.age > 35) riskScore += 2;
        if (data.age > 40) riskScore += 3;
        if (data.poids_kg > 100) riskScore += 1;
        if (data.antécédents === 'hypertension') riskScore += 3;
        if (data.antécédents === 'diabète') riskScore += 3;
        if (data.symptôme === 'douleur') riskScore += 2;
        
        // Calcul du niveau de risque
        let niveau, message;
        if (riskScore <= 2) {
            niveau = 'success';
            message = 'Risque faible. Continuez à prendre soin de vous et suivez les recommandations de votre médecin.';
        } else if (riskScore <= 5) {
            niveau = 'warning';
            message = 'Risque modéré. Surveillez vos symptômes et consultez régulièrement votre professionnel de santé.';
        } else {
            niveau = 'error';
            message = 'Risque élevé. Consultation médicale recommandée dans les plus brefs délais.';
        }
        
        return { niveau, message, score: riskScore };
    }
    
    showPredictionResult(result) {
        this.predictionResult.className = `prediction-result ${result.niveau}`;
        this.predictionResult.innerHTML = `
            <h3>Résultat de l'évaluation</h3>
            <p>${result.message}</p>
            ${result.score ? `<p><strong>Score de risque : ${result.score}/10</strong></p>` : ''}
        `;
        this.predictionResult.classList.remove('hidden');
        
        // Scroll vers le résultat
        this.predictionResult.scrollIntoView({ behavior: 'smooth' });
    }
}

// Initialisation de l'application
document.addEventListener('DOMContentLoaded', () => {
    new GrossesseAssistant();
    
    // Animation d'entrée
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease-in';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});"""
    
    with open(output_dir / "app.js", "w", encoding="utf-8") as f:
        f.write(js_content)

def create_surge_config(output_dir):
    """Crée la configuration Surge"""
    surge_config = {
        "project": "chatbot-grossesse",
        "domain": "chatbot-grossesse.surge.sh"
    }
    
    with open(output_dir / "surge.json", "w", encoding="utf-8") as f:
        json.dump(surge_config, f, indent=2)

def create_surge_readme(output_dir):
    """Crée le README pour Surge"""
    readme_content = """# 🚀 Déploiement Surge - Assistant Grossesse IA

## 📋 Prérequis

- Node.js installé sur votre machine
- Compte Surge (gratuit sur [surge.sh](https://surge.sh))

## 🔧 Installation de Surge

```bash
npm install -g surge
```

## 🌐 Déploiement

### 1. Aller dans le dossier de build
```bash
cd surge_build
```

### 2. Déployer sur Surge
```bash
surge
```

Suivez les instructions :
- **Email** : Votre email
- **Password** : Créez un mot de passe
- **Domain** : `chatbot-grossesse.surge.sh` (ou laissez Surge en choisir un)

### 3. Déploiement personnalisé
```bash
surge . --domain votre-nom.surge.sh
```

## 🔄 Mise à jour

Après modification des fichiers, redéployez :
```bash
surge
```

## 📱 Fonctionnalités

✅ **Chatbot IA** - Réponses intelligentes aux questions de grossesse  
✅ **Évaluation des risques** - Analyse basée sur les données personnelles  
✅ **Interface responsive** - Compatible mobile et desktop  
✅ **Design moderne** - Interface utilisateur intuitive et belle  

## 🎯 Avantages de Surge

- **Gratuit** et illimité
- **Déploiement instantané**
- **HTTPS automatique**
- **CDN global**
- **Domaine personnalisable**

## 🆘 Support

En cas de problème :
1. Vérifiez que Node.js est installé
2. Vérifiez votre connexion internet
3. Consultez la [documentation Surge](https://surge.sh/help)

---

**🎉 Votre Assistant Grossesse IA est maintenant en ligne !**"""
    
    with open(output_dir / "README_SURGE.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

if __name__ == "__main__":
    create_surge_app()

