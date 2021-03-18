from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from calculator_app.models import Calculations
from calculator_app.serializers import CalculationSerializer
import calculator_app.service

operation_list = ["add", "minus", "multiple", "divide"]

# def get_calculations(request):
#    calculations = Calculations.objects.all()
#    context = {
#        'calculations': calculations
#    }
#    return context


@api_view(["GET"])
def get_calculations(request):
    calculations = Calculations.objects.all()
    serializer = CalculationSerializer(calculations, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@parser_classes([JSONParser])
def calculate(request):
    data = {"numberA": request.data.get("numberA"), "numberB": request.data.get("numberB"),
            "operation": request.data.get("operation")}

    if not isinstance(data["numberA"], int) and not isinstance(data["numberA"], float):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif not isinstance(data["numberB"], int) and not isinstance(data["numberB"], float):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif data["operation"] not in operation_list:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    result = calculator_app.service.calculate(data)
    return Response(result)




