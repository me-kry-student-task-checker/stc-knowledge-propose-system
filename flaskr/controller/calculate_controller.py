from flask import Blueprint, request, abort
from flaskr.service import calculate_service

bp = Blueprint("calc", __name__, url_prefix="/calc")
operation_list = ["add", "minus", "multiple", "divide"]


@bp.route("/", methods=["POST"])
def calculate():
    content = request.json
    numberA = content["numberA"]
    numberB = content["numberB"]
    operation = content["operation"]

    print(type(numberA))
    print(type(numberB))

    if not isinstance(numberA, int) and not isinstance(numberA, float):
        abort(400, "First argument must be a number!")
    elif not isinstance(numberB, int) and not isinstance(numberB, float):
        abort(400, "Second argument must be a number!")
    elif operation not in operation_list:
        abort(400, "Operation must be add, minus, multiple or divide!")

    return calculate_service.calculate(numberA, numberB, operation)


@bp.route("/logs/", methods=["GET"])
def get_calculations():
    return calculate_service.get_calculations()
