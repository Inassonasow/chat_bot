from rest_framework import serializers

class GrossesseInputSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    mois_grossesse = serializers.IntegerField()
    poids_kg = serializers.FloatField()
    taille_cm = serializers.FloatField()
    activité = serializers.CharField()
    régime = serializers.CharField()
    antécédents = serializers.CharField()
    symptôme = serializers.CharField()
