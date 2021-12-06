import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

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
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html")
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html")
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        username = rows[0]["username"]
        # Redirect user to home page
        return render_template("index.html", username = username)
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
            return render_template("error.html")
        if not password:
            return render_template("error.html")
        if not confirmation:
            return render_template("error.html")
        # Ensure username is not taken
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            return render_template("error.html")
        # Ensure user verified password and check if passwords match
        if password != confirmation:
            return render_template("error.html")
        # Hash password
        hash = generate_password_hash(password)
        # Insert new user and log user in
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        return render_template("login.html")
    else:
        return render_template("register.html")

@app.route("/index")
@login_required
def index():
    # name = db.execute("SELECT username FROM users JOIN diary ON users.id = diary.user_id WHERE diary.user_id = ?", session["user_id"])[0]
    # username = name["username"]
    return render_template("index.html")

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
        #ask for today's goals
        daily_goals = request.form.get("daily_goals")
        #ask for dreams
        dream = request.form.get("dream")
        if request.form.get("sleep") == "1":
            sq = "Best Night Ever!!"
        elif request.form.get("sleep") == "2":
            sq = "Good"
        elif request.form.get("sleep") == "3":
            sq = "Eh.. it was okay"
        elif request.form.get("sleep") == "4":
            sq = "Not so great"
        elif request.form.get("sleep") == "5":
            sq = "Didn't sleep a wink T_T"
        sleep_quality = sq
        #ask for wake up mood
        if request.form.get("vibe") == "10":
            feelings = "excited"
        elif request.form.get("vibe") == "11":
            feelings = "happy"
        elif request.form.get("vibe") == "12":
            feelings = "ok"
        elif request.form.get("vibe") == "13":
            feelings = "sleepy"
        elif request.form.get("vibe") == "14":
            feelings = "sad"
        elif request.form.get("vibe") == "15":
            feelings = "tired"
        mood = feelings
        db.execute("INSERT INTO diary (user_id, hours_slept, snoozes, sleep_quality, mood, daily_goals, dream) VALUES (?,?,?,?,?,?,?)", session["user_id"], hours_slept, snoozes, sleep_quality, mood, daily_goals, dream)
        return render_template("submitted.html")
    else:
        # name = db.execute("SELECT username FROM users JOIN diary ON users.id = diary.user_id WHERE diary.user_id = ?", session["user_id"])[0]
        # username = name["username"]
        return render_template("diary.html")

@app.route("/log")
@login_required
def log():
    diarys = db.execute("SELECT * FROM diary WHERE user_id = :user_id ORDER BY time DESC", user_id=session["user_id"])
    return render_template("log.html", diarys = diarys)

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        new_password = request.form.get("new_password")
        new_password_confirmation = request.form.get("new_password_confirmation")
        if not new_password:
            return render_template("error.html")
        if not new_password_confirmation:
            return render_template("error.html")
        if new_password != new_password_confirmation:
            return render_template("error.html")
        new_password_hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_password_hash, session["user_id"])
        return render_template("changed.html", new_password_hash = new_password_hash)
    else:
        return render_template("change_password.html")

@app.route("/get_resources", methods=["GET", "POST"])
@login_required
def get_resources():
    if request.method == "POST":
        categories = request.form.getlist("tips")
        tips = []
        # find selected categories and add together
        for category in categories:
          sleep_tips = db.execute("SELECT category, source, link FROM tips WHERE category = ?", category)
          for dict in sleep_tips:
            tips.append(dict)
        return render_template("resources.html", tips = tips)
    else:
        return render_template("get_resources.html")

@app.route("/analysis")
@login_required
def analysis():
    avg_hours = db.execute("SELECT AVG(hours_slept) FROM diary WHERE user_id = ?", session["user_id"])[0]['AVG(hours_slept)']
    avg_snoozes = db.execute("SELECT AVG(snoozes) FROM diary WHERE user_id = ?", session["user_id"])[0]['AVG(snoozes)']
    #for the sleeping hour log
    time = []
    x = db.execute("SELECT time FROM diary WHERE user_id = ?", session["user_id"])
    for element in x:
        time.append(element["time"])
    hours = []
    y = db.execute("SELECT hours_slept FROM diary WHERE user_id = ?", session["user_id"])
    for element in y:
        hours.append(element["hours_slept"])
    #for sleep quality log
    A = db.execute("SELECT COUNT(sleep_quality) FROM diary WHERE user_id = ? AND sleep_quality = ?", session["user_id"], "Best Night Ever!!")[0]["COUNT(sleep_quality)"]
    B = db.execute("SELECT COUNT(sleep_quality) FROM diary WHERE user_id = ? AND sleep_quality = ?", session["user_id"], "Good")[0]["COUNT(sleep_quality)"]
    C = db.execute("SELECT COUNT(sleep_quality) FROM diary WHERE user_id = ? AND sleep_quality = ?", session["user_id"], "Eh.. it was okay")[0]["COUNT(sleep_quality)"]
    D = db.execute("SELECT COUNT(sleep_quality) FROM diary WHERE user_id = ? AND sleep_quality = ?", session["user_id"], "Not so great")[0]["COUNT(sleep_quality)"]
    E = db.execute("SELECT COUNT(sleep_quality) FROM diary WHERE user_id = ? AND sleep_quality = ?", session["user_id"], "Didn't sleep a wink")[0]["COUNT(sleep_quality)"]
    #for mood log
    Z = db.execute("SELECT COUNT(mood) FROM diary WHERE user_id = ? AND mood = ?", session["user_id"], "excited")[0]["COUNT(mood)"]
    Y = db.execute("SELECT COUNT(mood) FROM diary WHERE user_id = ? AND mood = ?", session["user_id"], "happy")[0]["COUNT(mood)"]
    X = db.execute("SELECT COUNT(mood) FROM diary WHERE user_id = ? AND mood = ?", session["user_id"], "ok")[0]["COUNT(mood)"]
    W = db.execute("SELECT COUNT(mood) FROM diary WHERE user_id = ? AND mood = ?", session["user_id"], "sleepy")[0]["COUNT(mood)"]
    S = db.execute("SELECT COUNT(mood) FROM diary WHERE user_id = ? AND mood = ?", session["user_id"], "sad")[0]["COUNT(mood)"]
    V = db.execute("SELECT COUNT(mood) FROM diary WHERE user_id = ? AND mood = ?", session["user_id"], "tired")[0]["COUNT(mood)"]
    return render_template("analysis.html", avg_hours = avg_hours, avg_snoozes = avg_snoozes, time = time, hours = hours, A = A, B = B, C = C, D = D, E = E, Z = Z, Y = Y, W = W, X = X, V = V, S = S)
 