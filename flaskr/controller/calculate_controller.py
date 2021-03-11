from flaskr.controller import validation
from flask import (
    Blueprint,
    request, abort
)
from flaskr.service import calculate_service

result = None
bp = Blueprint("calc", __name__, url_prefix="/calc")


@bp.route("/", methods=["POST"])
def calculate():
    content = request.json
    numberA = content["numberA"]
    numberB = content["numberB"]
    operation = content["operation"]

    error = None

    if content is None:
    abort(404)
     elif numberA.strip().isdigit():
        return calculate_service.calculate(numberA, numberB, operation)
    elif numberB.strip().isdigit():

    else:
    abort(403)




