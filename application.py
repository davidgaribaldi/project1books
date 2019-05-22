import os

from flask import Flask, session, render_template, request, redirect, url_for, Markup
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__, instance_relative_config=True)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

key = '2zsWV7eSAmEZzrujcsfQ'
secret = 'L2Snsbj1alSR0tWHHxAYUbd4zVTiUtWKrgZZIN5T1A'

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        value = Markup('<a class="btn btn-primary" href="logout" role="button">Logout</a>')
        search = Markup('<input type="text" name="search" placeholder="Search..." ><a class="btn btn-primary" href="results" role="button">Search</a>')
        return render_template("index.html", message='Logged in as ' + username, logout=value, search=search)
    login = Markup('<a class="btn btn-primary" href="login" role="button">Login Now</a>')
    register = Markup('<a class="btn btn-primary" href="register" role="button">Register</a>')
    return render_template("index.html", login=login, register=register)
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signin", methods=["POST"])
def signin():
    username = request.form.get("username")
    password = request.form.get("password")
    if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username":  str(username), "password": str(password)}).rowcount == 1:
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return "Not valid username or password"
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    session['username'] = username
    password = request.form.get("password")
    email = request.form.get("email")
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": str(username)}).rowcount == 1:
        return render_template("error.html", message="This username already exists")
    elif db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).rowcount == 1:
        return render_template("error.html", message="This email has already been used")
    elif len(password) < 6:
        return render_template("error.html", message="Passwords must be at least 6 characters")
    else:
        db.execute("INSERT INTO users (username, password, email) VALUES (:username, :password, :email)",
        {"username": username, "password": password, "email": email})
        session['username'] = username
        db.commit()
    return redirect(url_for('index'))


