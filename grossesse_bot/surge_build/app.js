// Application JavaScript pour l'Assistant Grossesse IA

class GrossesseAssistant {
    constructor() {
        console.log('🔧 Initialisation du constructeur...');
        this.initializeElements();
        this.bindEvents();
        this.loading = false;
        console.log('✅ Constructeur initialisé');
    }
    
    initializeElements() {
        console.log('🔍 Recherche des éléments...');
        
        this.chatInput = document.getElementById('chatInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.predictionForm = document.getElementById('predictionForm');
        this.predictionResult = document.getElementById('predictionResult');
        
        console.log('📝 Éléments trouvés:', {
            chatInput: !!this.chatInput,
            sendButton: !!this.sendButton,
            chatMessages: !!this.chatMessages,
            predictionForm: !!this.predictionForm,
            predictionResult: !!this.predictionResult
        });
    }
    
    bindEvents() {
        console.log('🔗 Liaison des événements...');
        
        if (this.sendButton) {
            this.sendButton.addEventListener('click', () => {
                console.log('📤 Bouton d\'envoi cliqué');
                this.sendMessage();
            });
            console.log('✅ Événement click ajouté au bouton d\'envoi');
        }
        
        if (this.chatInput) {
            this.chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    console.log('⌨️ Touche Entrée pressée');
                    this.sendMessage();
                }
            });
            console.log('✅ Événement keypress ajouté au champ de saisie');
        }
        
        if (this.predictionForm) {
            this.predictionForm.addEventListener('submit', (e) => {
                console.log('📋 Formulaire soumis');
                this.handlePrediction(e);
            });
            console.log('✅ Événement submit ajouté au formulaire');
        }
        
        console.log('✅ Tous les événements ont été liés');
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
        return "Je comprends votre preoccupation. Pour des conseils personnalises, n'hesitez pas a me donner plus de details sur votre situation. N'oubliez pas que je ne remplace pas l'avis medical de votre professionnel de sante.";
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
        
        // Afficher un message de chargement
        this.showPredictionResult({
            niveau: 'warning',
            message: '⏳ Évaluation en cours...'
        });
        
        const formData = new FormData(this.predictionForm);
        const data = {
            age: parseInt(formData.get('age')),
            mois_grossesse: parseInt(formData.get('mois_grossesse')),
            poids_kg: parseFloat(formData.get('poids_kg')),
            taille_cm: parseInt(formData.get('taille_cm')),
            activite: formData.get('activite'),
            regime: formData.get('regime'),
            antecedents: formData.get('antecedents'),
            symptome: formData.get('symptome')
        };
        
        // Debug: afficher les données reçues
        console.log('Données du formulaire:', data);
        
        try {
            const result = await this.predictRisk(data);
            this.showPredictionResult(result);
        } catch (error) {
            this.showPredictionResult({
                niveau: 'error',
                message: 'Erreur lors de l\'evaluation. Veuillez reessayer.'
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
        if (data.antecedents === 'hypertension') riskScore += 3;
        if (data.antecedents === 'diabète') riskScore += 3;
        if (data.symptome === 'douleur') riskScore += 2;
        
        // Calcul du niveau de risque
        let niveau, message;
        if (riskScore <= 2) {
            niveau = 'success';
            message = 'Risque faible. Continuez a prendre soin de vous et suivez les recommandations de votre medecin.';
        } else if (riskScore <= 5) {
            niveau = 'warning';
            message = 'Risque modere. Surveillez vos symptomes et consultez regulierement votre professionnel de sante.';
        } else {
            niveau = 'error';
            message = 'Risque eleve. Consultation medicale recommandee dans les plus brefs delais.';
        }
        
        return { niveau, message, score: riskScore };
    }
    
    showPredictionResult(result) {
        this.predictionResult.className = `prediction-result ${result.niveau}`;
        this.predictionResult.innerHTML = `
            <h3>Resultat de l'evaluation</h3>
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
    console.log('🚀 DOM chargé, initialisation de l\'application...');
    
    try {
        new GrossesseAssistant();
        console.log('✅ Application initialisée avec succès');
    } catch (error) {
        console.error('❌ Erreur lors de l\'initialisation:', error);
    }
    
    // Animation d'entrée
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease-in';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});