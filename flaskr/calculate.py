from flask import (
    Blueprint,
    request
)
from . import calculate_service

result = None
bp = Blueprint("calc", __name__, url_prefix="/calc")


@bp.route("/", methods=["POST"])
def calculate():
    content = request.json
    numberA = content["numberA"]
    numberB = content["numberB"]
    operation = content["operation"]

    error = None
    if not numberA:
        error = "Number A is required"
    elif not numberB:
        error = "Number B is required"

    return calculate_service.calculate(numberA, numberB, operation)
