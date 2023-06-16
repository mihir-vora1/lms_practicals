from rest_framework import serializers
from .models import Purchase, Restrict

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

class RestrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restrict
        fields = '__all__'