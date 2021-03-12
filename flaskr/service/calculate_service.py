from flask import jsonify, abort


def calculate(numberA, numberB, operation):
    result = None

    if numberB == 0 and operation == "divide":
        abort(400, "You can't divide with zero")

    if operation == "add":
        result = numberA + numberB
    elif operation == "minus":
        result = numberA - numberB
    elif operation == "multiple":
        result = numberA * numberB
    elif operation == "divide":
        result = numberA / numberB

    return jsonify({"result": result})
