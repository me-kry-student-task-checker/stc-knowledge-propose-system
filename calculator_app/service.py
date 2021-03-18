from rest_framework import status
from rest_framework.response import Response


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

    ##calculate_dao.insert_result(numberA, numberB, operation, result)

    return {"result": result}
