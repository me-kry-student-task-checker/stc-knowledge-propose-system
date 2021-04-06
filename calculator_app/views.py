from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from calculator_app.models import Calculations
from calculator_app.serializers import CalculationSerializer
from calculator_app import service


@api_view(["POST"])
def recommend_books(request):
    user_id = request.data.get("userid")

    try:
        service.validate_bookuser_input(user_id)
        result = service.recommend_books(user_id)
    except (ZeroDivisionError, ValidationError) as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(result)


@api_view(["GET"])
def get_calculations(request):
    calculations = Calculations.objects.all()
    serializer = CalculationSerializer(calculations, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def calculate(request):
    data = {"numberA": request.data.get("numberA"), "numberB": request.data.get("numberB"),
            "operation": request.data.get("operation"), "result": None}

    try:
        service.validate_input(data)
        result = service.calculate(data)
    except (ZeroDivisionError, ValidationError) as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(result)
