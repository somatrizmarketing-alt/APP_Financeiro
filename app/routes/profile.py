from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile")
@login_required
def perfil():
    return render_template("perfil.html", user=current_user)


@profile_bp.route("/alterar-senha", methods=["POST"])
@login_required
def alterar_senha():
    senha_atual = request.form.get("senha_atual")
    nova_senha = request.form.get("nova_senha")

    if not check_password_hash(current_user.password, senha_atual):
        flash("Senha incorreta")
        return redirect(url_for("profile.perfil"))

    current_user.password = generate_password_hash(nova_senha)
    db.session.commit()

    flash("Senha alterada!")
    return redirect(url_for("profile.perfil"))