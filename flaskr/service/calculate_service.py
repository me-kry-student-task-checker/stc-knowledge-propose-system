from flask import jsonify, abort
from flaskr.dao import calculate_dao


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

    calculate_dao.insert_result(numberA, numberB, operation, result)

    return jsonify({"result": result})


def get_calculations():
    return jsonify(calculate_dao.get_calculations())
