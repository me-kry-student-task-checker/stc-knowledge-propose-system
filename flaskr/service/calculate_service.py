from flask import jsonify


def calculate(numberA, numberB, operation):
    result = None

    if operation == "add":
        result = numberA + numberB
    elif operation == "minus":
        result = numberA - numberB
    elif operation == "multiple":
        result = numberA * numberB
    elif operation == "divide":
        result = numberA / numberB

    return jsonify({"result": result})
