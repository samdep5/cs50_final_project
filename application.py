import os
from datetime import datetime, date, timedelta
import pytz

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///plants.db")


@app.route("/")
@login_required
def plant():
    """Show plants"""

    # Query database for user's plants
    plants = db.execute("""SELECT name, id, frequency,
                        STRFTIME('%m/%d/%Y', startdate) AS date
                        FROM plant WHERE user_id = ?""",  session["user_id"])

    # Find the next watering date of each plant
    for plant in plants:
        # Find current date considering the user's timezone
        currentdate = datetime.now(pytz.timezone(db.execute(
            "SELECT timezone FROM users WHERE id=?", session["user_id"])[0]["timezone"])).date()
        print(currentdate)
        # Create list of structure [month, day, year] of plant's startdate
        elements = plant["date"].split("/")

        # Calculate integer difference between the current date and plant's watering start date
        nextwater = int((currentdate - date(int(elements[2]), int(elements[0]), int(elements[1]))).days)
        print(nextwater)

        frequency = plant['frequency']

        # If startdate is in the future set next watering as startdate
        if nextwater < 0:
            plant["watermessage"] = "Next Watering is on " + plant["date"]

        # If difference between current and start date divided by frequency has no remainder watering is today
        elif nextwater % frequency == 0:
            plant["watermessage"] = "Watering is Today!"

        else:
            resultdate = currentdate
            # If current and start date difference is greater than frequency calculate next watering accordingly
            if nextwater > frequency:
                resultdate = resultdate + timedelta(-(nextwater % frequency) + frequency)

            # If nextwater is less than frequency calculate next watering accordingly
            else:
                resultdate = resultdate + timedelta(frequency - nextwater)

            # Save date message in table
            plant["watermessage"] = resultdate.strftime("Next Watering is on %m/%d/%Y")

    # Render
    return render_template("index.html", plants=plants)


@app.route("/addplant", methods=["GET", "POST"])
@login_required
def addplant():
    """Enable user add a plant."""

    # POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("name"):
            return apology("missing name")

        # Ensure plant name is unique
        elif db.execute("SELECT id FROM plant WHERE name=? AND user_id=?", request.form.get("name").lower(), session["user_id"]):
            return apology("plant name is a copy")

        # Ensure frequency was submitted
        elif not request.form.get("frequency"):
            return apology("missing watering frequency")

        # Ensure startdate was submitted
        elif not request.form.get("startdate"):
            return apology("missing start date")

        # Create variables for form entries
        startdate = request.form.get("startdate")
        frequency = request.form.get("frequency")
        name = request.form.get("name")

        # Record new plant in plant table
        db.execute("INSERT INTO plant (user_id, frequency, name, startdate) VALUES(?, ?, ?, ?)",
                   session["user_id"], frequency, name, startdate)

        # Display plants
        flash("New plant added!")
        return redirect("/")

    # GET
    else:
        return render_template("addplant.html")


@app.route("/editfields", methods=["GET", "POST"])
@login_required
def editplant():
    """Enable user edit a plant."""

    # POST
    if request.method == "POST":

        check = 0
        # Ensure plant is selected
        if not request.form.get("names"):
            return apology("Must select a plant")

        # Update name if requested
        if request.form.get("editname"):
            check += 1
            db.execute("UPDATE plant SET name=? WHERE id=?", str(request.form.get("editname").lower()), request.form.get("names"))

        # Update startdate if requested
        if request.form.get("editdate"):
            check += 1
            db.execute("UPDATE plant SET startdate=? WHERE id=?", request.form.get("editdate"), request.form.get("names"))

        # Update frequency if requested
        if request.form.get("editfrequency"):
            check += 1
            db.execute("UPDATE plant SET frequency=? WHERE id=?", request.form.get("editfrequency"), request.form.get("names"))

        # Ensure at least one field was altered
        if check == 0:
            return apology("Must change at least one field")

        # Flash update and redirect
        flash("Plant updated!")
        return redirect("/")

    # GET
    else:
        # Get user's plant values t display in dropdown
        plants = db.execute("SELECT name, id FROM plant WHERE user_id=?", session["user_id"])

        return render_template("editfields.html", plants=plants)


@app.route("/deleteplant", methods=["GET", "POST"])
@login_required
def deleteplant():
    """Enable user to delete a plant."""

    # POST
    if request.method == "POST":

        # Ensure plant selection
        if not request.form.get("names"):
            return apology("missing name")

        # Delete plant
        db.execute("DELETE FROM plant WHERE id=?", request.form.get("names"))

        # Display plants and flash delete
        flash("Plant deleted")
        return redirect("/")

    # GET
    else:
        plants = db.execute("SELECT name, id FROM plant WHERE user_id=?", session["user_id"])
        return render_template("deleteplant.html", plants=plants)


@app.route("/deletejournal", methods=["GET", "POST"])
@login_required
def deletejournal():
    """Enable user delete a journal entry."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("entry"):
            return apology("must select entry")

        entry_id = request.form.get("entry")

        # Delete plant
        db.execute("DELETE FROM journal WHERE id=?", request.form.get("entry"))

        # Display journal entries
        flash("Entry deleted")
        return redirect("/journal")

    # GET
    else:
        journal = db.execute("SELECT * FROM journal WHERE user_id=? ORDER BY date DESC", session["user_id"])
        return render_template("deletejournal.html", journal=journal)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # POST
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

    # GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("missing username")

        # Ensure username was not already taken
        elif db.execute("SELECT id FROM users WHERE username=?", str(request.form.get("username")).lower()):
            return apology("username is already taken")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("missing password")

        # Ensure password matches confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Ensure timezone is entered
        elif not request.form.get("timezone_offset"):
            return apology("missing timezone")

        # Add user to users database
        id = db.execute("INSERT INTO users (username, hash, timezone) VALUES(?, ?, ?)",
                        request.form.get("username"),
                        generate_password_hash(request.form.get("password")),
                        request.form.get("timezone_offset"))

        # Log user in
        session["user_id"] = id

        # ALert user registered
        flash("Registered!")
        return redirect("/")

    # GET
    else:
        return render_template("register.html")


@app.route("/journal")
@login_required
def journal():
    """Enable user to journal."""

    # Select all journal entries to display
    journal = db.execute("SELECT * FROM journal WHERE user_id=? ORDER BY date", session["user_id"])

    return render_template("journal.html", journal=journal)


@app.route("/journalentry", methods=["GET", "POST"])
@login_required
def journalentry():
    """Add new journal entry about plants."""
    # POST
    if request.method == "POST":

        # Ensure title was submitted
        if not request.form.get("title"):
            return apology("must enter a title")

        # Ensure entry was submitted
        elif not request.form.get("entry"):
            return apology("missing notes")

        # Insert new journal entry into SQL database
        db.execute("INSERT INTO journal (user_id, entry, title, date) VALUES(?, ?, ?, ?)",
                   session["user_id"], request.form.get("entry"), request.form.get("title"),
                   datetime.now(pytz.timezone(db.execute("SELECT timezone FROM users WHERE id=?", session["user_id"])[0]["timezone"])).date())

        return redirect("/journal")

    else:
        return render_template("journalentry.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

