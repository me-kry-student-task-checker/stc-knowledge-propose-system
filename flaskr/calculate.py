from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

result = None
bp = Blueprint("calc", __name__, url_prefix="/calc")


@bp.route("/", methods=("GET", "POST"))
def calculate():
    if request.method == "POST":
        numberA = int(request.form["numberA"])
        numberB = int(request.form["numberB"])
        operation = request.form["operation"]

        error = None
        if not numberA:
            error = "Number A is required"
        elif not numberB:
            error = "Number B is required"
        else:
            result = numberA + numberB

        if operation == "add":
            result = numberA + numberB
        elif operation == "minus":
            result = numberA - numberB
        elif operation == "multiple":
            result = numberA * numberB
        elif operation == "divide":
            result = numberA / numberB

        session.clear()
        session["result"] = result
        # return redirect(url_for("hello"))
    return render_template("base.html")
