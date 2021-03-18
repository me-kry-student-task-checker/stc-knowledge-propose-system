from rest_framework import status
from rest_framework.response import Response

from calculator_app.serializers import CalculationSerializer


def calculate(data):
    result = None
    numberA = data["numberA"]
    numberB = data["numberB"]
    operation = data["operation"]

    if numberB == 0 and operation == "divide":
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if operation == "add":
        result = numberA + numberB
    elif operation == "minus":
        result = numberA - numberB
    elif operation == "multiple":
        result = numberA * numberB
    elif operation == "divide":
        result = numberA / numberB

    db_data = {"numbera": numberA, "numberb": numberB, "operation": operation, "result": result}
    serializer = CalculationSerializer(data=db_data)
    if serializer.is_valid():
        serializer.save()

    return {"result": result}
