from flask import Flask, render_template, redirect, session
from forms import RegisterForm, PasswordForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

#----db creation----
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, "instance")

if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(instance_path, "user.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "sasa"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
#----ROUTES----
@app.route("/")
def home():
    return render_template("main.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/books")
def books():
    if session.get("logged_in"):
        book_links = [
            {
                "title": "ukharkhasho khmlebi",
                "description": "A classic Georgian historical text.",
                "url": "https://dspace.nplg.gov.ge/handle/1234/87843"
            },
            {
                "title": "kartlis ckhovreba",
                "description": "The medieval Georgian chronicle describing kings and history.",
                "url": "https://dspace.nplg.gov.ge/handle/1234/315448"
            },
            {
                "title": "vefkhis tkaosani",
                "description": "An interesting historical book about Georgia.",
                "url": "https://drive.google.com/file/d/0BwCMyTECcJPnTGk3WjY0VUpaMTg/view?resourcekey=0-B-tEOPzvFUx-W0GWlMV_EA"
            }
        ]
        return render_template("books.html", book_links=book_links)
    else:
        return render_template("books.html", book_links=None)

#-singup-
@app.route("/login", methods=["GET", "POST"])
def login():
    form = PasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["logged_in"] = True
            session["username"] = email
            return redirect("/login-success")

    return render_template("login.html", form=form)

@app.route("/login-success")
def login_success():
    if not session.get("logged_in"):
        return redirect("/login")

    return render_template("login_success.html", username=session.get("username"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/daily-history")
def daily_history():
    logged_in = True
    return render_template(
        "dailyhistory.html",
        day1_link="https://en.wikipedia.org/wiki/Colchis",
        day2_link="https://example.com/day2",
        day3_link="https://example.com/day3",
        logged_in=logged_in
    )
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = generate_password_hash(form.password.data)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("register.html", form=form, error="Email already registered!")

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template("success.html", username=email)

    return render_template("register.html", form=form)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)