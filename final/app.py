import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///sleeps50.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
      
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Ensure user input information properly
        if not username:
            return apology("Must provide username", 400)
        if not password:
            return apology("Must provide password", 400)
        if not confirmation:
            return apology("Must provide confirmation", 400)
        # Ensure username is not taken
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            return apology("Username already exists", 400)
        # Ensure user verified password and check if passwords match
        if password != confirmation:
            return apology("Passwords must match", 400)
        # Hash password
        hash = generate_password_hash(password)
        # Insert new user and log user in
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        return redirect("/")
    else:
        return render_template("register.html")

def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


#SECOND PAGE FUNCTIONALITIES
@app.route("/diary", methods=["GET", "POST"])
@login_required
def diary():
    if request.method == "POST":
        #ask for hours slept
        hours_slept = request.form.get("hours_slept")
        #ask for number of snoozes
        snoozes = request.form.get("snoozes")
        #ask for sleep quality
        # sleep_quality = request.form.get("sleep_quality")
        sleep_quality = "good"
        #ask for wake up mood
        # mood = request.form.get("mood")
        mood = "good"
        #ask for today's goals
        daily_goals = request.form.get("daily_goals")
        #ask for dreams
        dream = request.form.get("dream")
        #query into diary database
        db.execute("INSERT INTO diary (user_id, hours_slept, snoozes, sleep_quality, mood, daily_goals, dream) VALUES (?,?,?,?,?,?,?)", session["user_id"], hours_slept, snoozes, sleep_quality, mood, daily_goals, dream)
        return redirect("log.html") #might have to change this later (jolin: i changed it to log)
    else:
        return render_template("diary.html")

@app.route("/log")
@login_required
def log():
    diary_log = db.execute("SELECT * FROM diary WHERE id = ?", session["user_id"])
    return render_template("log.html", diary_log = diary_log)
        
