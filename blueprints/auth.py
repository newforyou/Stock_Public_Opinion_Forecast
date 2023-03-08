from flask import Blueprint, render_template, request
from .forms import RegisterForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            return "success"
        else:
            print(form.errors)
            return "fail"
