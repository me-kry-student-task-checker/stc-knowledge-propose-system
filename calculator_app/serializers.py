from rest_framework import serializers
from calculator_app.models import Calculations


class CalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculations
        fields = ("numbera", "numberb", "operation", "result")


