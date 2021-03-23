from rest_framework.exceptions import ValidationError

from calculator_app.serializers import CalculationSerializer


def calculate(data):
    result = None
    numberA = data["numberA"]
    numberB = data["numberB"]
    operation = data["operation"]

    if operation == "add":
        result = numberA + numberB
    elif operation == "minus":
        result = numberA - numberB
    elif operation == "multiple":
        result = numberA * numberB
    elif operation == "divide":
        result = numberA / numberB

    data["result"] = result
    serializer = CalculationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

    return {"result": result}


def validate_input(data):
    operation_list = ["add", "minus", "multiple", "divide"]

    if not isinstance(data["numberA"], int) and not isinstance(data["numberA"], float):
        raise ValidationError
    elif not isinstance(data["numberB"], int) and not isinstance(data["numberB"], float):
        raise ValidationError
    elif data["operation"] not in operation_list:
        raise ValidationError
    elif data["numberB"] == 0 and data["operation"] == "divide":
        raise ZeroDivisionError
