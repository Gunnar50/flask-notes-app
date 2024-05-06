from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    message = {"text": "", "category": ""}
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in succefully.", category="success")
                message["text"] = "Logged in succefully."
                message["category"] = "success"
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
                
        flash("Wrong email or password.", category="error")
        message["text"] = "Wrong email or password."
        message["category"] = "error"
                
    return render_template("login.html", user=current_user, **message)


@auth.route("/register", methods=["GET", "POST"])
def register():
    message = {"text": "", "category": ""}
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirmation = request.form.get("password2")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email address already registered, please login.", category="error")
            message["text"] = "Email address already registered, please login."
            message["category"] = "error"
            
        elif len(email) < 4:
            flash("Email address must be at least 4 characters.", category="error")
            message["text"] = "Email address must be at least 4 characters"
            message["category"] = "error"

        elif len(password) < 5:
            flash("Password must be at least 5 characters", category="error")
            message["text"] = "Password must be at least 5 characters"
            message["category"] = "error"

        elif password != password_confirmation:
            flash("Passwords do not match.", category="error")
            message["text"] = "Passwords do not match."
            message["category"] = "error"
            
        else:
            new_user = User(email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            message["text"] = "Account created!"
            message["category"] = "success"
            login_user(user, remember=True)
            return redirect(url_for("views.home"))

    return render_template("register.html", **message, user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
