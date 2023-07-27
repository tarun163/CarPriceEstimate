from .models import CarValueData, EstimatedData
from rest_framework import serializers

class CarValueDataSerializer(serializers.Serializer):
    
    class Meta:
        model = CarValueData