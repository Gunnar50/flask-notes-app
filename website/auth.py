from flask import Blueprint, render_template, request, flash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        print(data)
    return render_template("login.html", text="Testing")


@auth.route("/register", methods=["GET", "POST"])
def register():
    message = {"text": "", "category": ""}
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirmation = request.form.get("password2")

        if len(email) < 4:
            flash("Email address must be at least 4 characters.", category="error")
            message["text"] = "Email address must be at least 4 characters"
            message["category"] = "error"

        if len(password) < 5:
            flash("Password must be at least 5 characters", category="error")
            message["text"] = "Password must be at least 5 characters"
            message["category"] = "error"

        if password != password_confirmation:
            flash("Passwords do not match.", category="error")
            message["text"] = "Passwords do not match."
            message["category"] = "error"

        flash("Account created!", category="success")
        message["text"] = "Account created!"
        message["category"] = "success"

    return render_template("register.html", **message)


@auth.route("/logout")
def logout():
    return "<p>Logout</p>"
