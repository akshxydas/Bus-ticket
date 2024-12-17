from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret"  # Secret key for sessions (required)

# Dummy credentials
VALID_USER = {"username": "user", "password": "password"}
VALID_MANAGER = {"username": "manager", "password": "admin123"}

# Simulated data
FARES = {
    ("City A", "City B"): 50,
    ("City A", "City C"): 80,
    ("City B", "City C"): 30
}

# Data to track booked tickets
bus_passengers = 0


# Login route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # User login
        if username == VALID_USER["username"] and password == VALID_USER["password"]:
            session["user"] = username
            return redirect(url_for("dashboard"))

        # Manager login
        elif username == VALID_MANAGER["username"] and password == VALID_MANAGER["password"]:
            session["manager"] = username
            return redirect(url_for("manager_dashboard"))

        else:
            return "Invalid credentials, please try again."

    return render_template("login.html")


# User Dashboard route
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))  # Redirect if not logged in

    fare = None
    if request.method == "POST":
        from_location = request.form.get("from")
        to_location = request.form.get("to")
        fare = FARES.get((from_location, to_location), "Fare not available")
        session["from"] = from_location
        session["to"] = to_location
        session["fare"] = fare

    return render_template("dashboard.html", fare=fare)


# Book ticket route
@app.route("/book_ticket", methods=["GET", "POST"])
def book_ticket():
    global bus_passengers

    if "user" not in session or "fare" not in session:
        return redirect(url_for("dashboard"))  # Redirect if no fare selected

    if request.method == "POST":
        bus_passengers += 1  # Simulate adding a passenger
        return f"Payment successful! Ticket booked from {session['from']} to {session['to']} for ${session['fare']}."

    return render_template("book_ticket.html", fare=session["fare"], from_location=session["from"], to_location=session["to"])


# Bus Manager Dashboard route
@app.route("/manager_dashboard")
def manager_dashboard():
    if "manager" not in session:
        return redirect(url_for("login"))

    return render_template("manager_dashboard.html", passengers=bus_passengers)


# Logout route
@app.route("/logout")
def logout():
    session.clear()  # Clear all sessions
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
