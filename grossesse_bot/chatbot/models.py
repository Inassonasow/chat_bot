from django.db import models
from django.db import models

class EvaluationGrossesse(models.Model):
    age = models.IntegerField()
    mois_grossesse = models.IntegerField()
    poids_kg = models.FloatField()
    taille_cm = models.FloatField()
    activité = models.CharField(max_length=20)
    régime = models.CharField(max_length=20)
    antécédents = models.CharField(max_length=50)
    symptôme = models.CharField(max_length=30)
    profil_risque = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.age} ans - Risque: {self.profil_risque}"

# Create your models here.
