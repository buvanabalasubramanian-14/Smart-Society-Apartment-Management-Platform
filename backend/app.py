from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

# =========================================================
# CONFIGURATION
# =========================================================

app.config["SECRET_KEY"] = "smart-society-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///smart_society.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================================================
# DATABASE MODEL
# =========================================================

class Resident(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    flat_no = db.Column(
        db.String(20),
        nullable=False
    )

    phone = db.Column(
        db.String(10),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


# =========================================================
# COMMON CSS
# =========================================================

STYLE = """

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #f5f7fb;
    color: #1e293b;
}


/* NAVBAR */

.navbar {
    background: #172554;
    color: white;
    height: 70px;

    display: flex;
    align-items: center;

    padding: 0 8%;
}

.logo {
    font-size: 23px;
    font-weight: bold;
}


/* MAIN CONTAINER */

.container {
    width: 90%;
    max-width: 1100px;

    margin: 50px auto;
}


/* HERO */

.hero {
    background: white;

    padding: 65px 40px;

    border-radius: 20px;

    text-align: center;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.08);

    border: 1px solid #e2e8f0;
}

.hero-icon {
    font-size: 55px;
    margin-bottom: 10px;
}

.hero h1 {
    color: #172554;

    font-size: 44px;

    margin: 5px 0 10px;
}

.hero h2 {
    color: #475569;

    font-size: 24px;

    font-weight: normal;

    margin: 0 0 20px;
}

.hero p {
    color: #64748b;

    max-width: 650px;

    margin: 0 auto;

    line-height: 1.7;

    font-size: 16px;
}


/* BUTTON */

.btn {
    display: inline-block;

    padding: 13px 28px;

    border-radius: 8px;

    background: #2563eb;

    color: white;

    text-decoration: none;

    border: none;

    cursor: pointer;

    font-size: 15px;

    font-weight: bold;

    margin: 5px;
}

.btn:hover {
    background: #1d4ed8;
}

.btn-secondary {
    background: #e2e8f0;

    color: #1e293b;
}

.btn-secondary:hover {
    background: #cbd5e1;
}


/* FEATURE CARDS */

.features {
    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 20px;

    margin-top: 30px;
}

.module {
    background: white;

    padding: 28px;

    border-radius: 15px;

    border: 1px solid #e2e8f0;

    box-shadow:
        0 6px 20px rgba(0, 0, 0, 0.06);
}

.module-icon {
    font-size: 32px;
}

.module h3 {
    color: #172554;

    margin: 12px 0;
}

.module p {
    color: #64748b;

    line-height: 1.6;

    font-size: 14px;
}


/* FORM CARD */

.card {
    background: white;

    width: 100%;

    max-width: 500px;

    margin: 50px auto;

    padding: 40px;

    border-radius: 18px;

    border: 1px solid #e2e8f0;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.08);
}

.card h2 {
    text-align: center;

    color: #172554;

    margin-bottom: 30px;
}


/* FORM */

label {
    display: block;

    margin-bottom: 7px;

    font-weight: bold;

    color: #334155;
}

input {
    width: 100%;

    padding: 12px;

    margin-bottom: 20px;

    border: 1px solid #cbd5e1;

    border-radius: 8px;

    font-size: 15px;
}

input:focus {
    outline: none;

    border-color: #2563eb;

    box-shadow:
        0 0 0 3px
        rgba(37, 99, 235, 0.10);
}

.full-btn {
    width: 100%;

    margin: 0;
}


/* MESSAGES */

.error {
    background: #fee2e2;

    color: #991b1b;

    padding: 15px;

    border-radius: 8px;

    margin-bottom: 20px;
}

.success {
    background: #dcfce7;

    color: #166534;

    padding: 15px;

    border-radius: 8px;

    margin-bottom: 20px;
}


/* DASHBOARD */

.dashboard-header {
    background: #172554;

    color: white;

    padding: 30px;

    border-radius: 18px;

    margin-bottom: 30px;
}

.dashboard-header h1 {
    margin: 0 0 8px;
}

.dashboard-header p {
    margin: 0;

    color: #dbeafe;
}


/* FOOTER */

.footer {
    text-align: center;

    color: #64748b;

    font-size: 13px;

    margin: 40px 0;
}


/* MOBILE */

@media (max-width: 750px) {

    .features {
        grid-template-columns: 1fr;
    }

    .hero h1 {
        font-size: 34px;
    }

    .hero h2 {
        font-size: 20px;
    }

    .navbar {
        padding: 0 5%;
    }
}

</style>
"""


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return STYLE + """

    <div class="navbar">

        <div class="logo">
            Smart Society
        </div>

    </div>


    <div class="container">

        <div class="hero">

            <div class="hero-icon">
                🏢
            </div>

            <h1>
                Smart Society
            </h1>

            <h2>
                Apartment Management Platform
            </h2>

            <p>
                A secure and convenient platform for
                managing residential community services,
                resident information and apartment activities.
            </p>


            <div style="margin-top: 30px;">

                <a
                    class="btn"
                    href="/register"
                >
                    Get Started
                </a>

                <a
                    class="btn btn-secondary"
                    href="/login"
                >
                    Resident Login
                </a>

            </div>

        </div>


        <div class="features">


            <div class="module">

                <div class="module-icon">
                    🏠
                </div>

                <h3>
                    Resident Management
                </h3>

                <p>
                    Secure resident registration and
                    account management for apartment
                    residents.
                </p>

            </div>


            <div class="module">

                <div class="module-icon">
                    📝
                </div>

                <h3>
                    Complaint Management
                </h3>

                <p>
                    Residents can raise and track
                    apartment-related complaints.
                </p>

            </div>


            <div class="module">

                <div class="module-icon">
                    👥
                </div>

                <h3>
                    Visitor Management
                </h3>

                <p>
                    Maintain visitor information and
                    visit records efficiently.
                </p>

            </div>


        </div>

    </div>


    <div class="footer">

        © 2026 Smart Society |
        Apartment Management Platform

    </div>

    """


# =========================================================
# RESIDENT REGISTRATION
# CORE FUNCTION 1
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"].strip()

        flat_no = request.form["flat_no"].strip()

        phone = request.form["phone"].strip()

        email = request.form["email"].strip().lower()

        password = request.form["password"]


        # -------------------------------
        # NAME VALIDATION
        # -------------------------------

        if not re.fullmatch(
            r"[A-Za-z ]+",
            name
        ):

            return STYLE + """

            <div class="container">

                <div class="card">

                    <div class="error">

                        <strong>
                            Invalid Name
                        </strong>

                        <br><br>

                        Please enter a valid name
                        using letters only.

                    </div>

                    <a
                        class="btn full-btn"
                        href="/register"
                    >
                        Go Back
                    </a>

                </div>

            </div>

            """


        # -------------------------------
        # PHONE VALIDATION
        # -------------------------------

        if not re.fullmatch(
            r"[0-9]{10}",
            phone
        ):

            return STYLE + """

            <div class="container">

                <div class="card">

                    <div class="error">

                        <strong>
                            Invalid Phone Number
                        </strong>

                        <br><br>

                        Please enter a valid
                        10-digit phone number.

                    </div>

                    <a
                        class="btn full-btn"
                        href="/register"
                    >
                        Go Back
                    </a>

                </div>

            </div>

            """


        # -------------------------------
        # PASSWORD VALIDATION
        # -------------------------------

        if len(password) < 6:

            return STYLE + """

            <div class="container">

                <div class="card">

                    <div class="error">

                        <strong>
                            Invalid Password
                        </strong>

                        <br><br>

                        Password must contain
                        at least 6 characters.

                    </div>

                    <a
                        class="btn full-btn"
                        href="/register"
                    >
                        Go Back
                    </a>

                </div>

            </div>

            """


        # -------------------------------
        # CHECK EMAIL
        # -------------------------------

        existing_resident = Resident.query.filter_by(
            email=email
        ).first()


        if existing_resident:

            return STYLE + """

            <div class="container">

                <div class="card">

                    <div class="error">

                        <strong>
                            Email Already Registered
                        </strong>

                        <br><br>

                        Please use another email
                        address.

                    </div>

                    <a
                        class="btn full-btn"
                        href="/register"
                    >
                        Go Back
                    </a>

                </div>

            </div>

            """


        # -------------------------------
        # HASH PASSWORD
        # -------------------------------

        hashed_password = generate_password_hash(
            password
        )


        # -------------------------------
        # CREATE RESIDENT
        # -------------------------------

        resident = Resident(

            name=name,

            flat_no=flat_no,

            phone=phone,

            email=email,

            password=hashed_password

        )


        db.session.add(resident)

        db.session.commit()


        return STYLE + """

        <div class="container">

            <div class="card">

                <div class="success">

                    <strong>
                        Registration Successful!
                    </strong>

                    <br><br>

                    Your resident account has
                    been created successfully.

                </div>


                <a
                    class="btn full-btn"
                    href="/login"
                >
                    Continue to Login
                </a>

            </div>

        </div>

        """


    # =====================================================
    # REGISTRATION FORM
    # =====================================================

    return STYLE + """

    <div class="navbar">

        <div class="logo">
            Smart Society
        </div>

    </div>


    <div class="container">

        <div class="card">

            <h2>
                Resident Registration
            </h2>


            <form method="POST">


                <label>
                    Full Name
                </label>

                <input
                    type="text"
                    name="name"
                    required
                    pattern="[A-Za-z ]+"
                    title="Please enter a valid name using letters only"
                    placeholder="Enter your full name"
                >


                <label>
                    Flat Number
                </label>

                <input
                    type="text"
                    name="flat_no"
                    required
                    placeholder="Example: A-101"
                >


                <label>
                    Phone Number
                </label>

                <input
                    type="tel"
                    name="phone"
                    required
                    pattern="[0-9]{10}"
                    maxlength="10"
                    placeholder="Enter 10-digit phone number"
                >


                <label>
                    Email Address
                </label>

                <input
                    type="email"
                    name="email"
                    required
                    placeholder="example@email.com"
                >


                <label>
                    Password
                </label>

                <input
                    type="password"
                    name="password"
                    required
                    minlength="6"
                    placeholder="Minimum 6 characters"
                >


                <button
                    class="btn full-btn"
                    type="submit"
                >
                    Create Resident Account
                </button>


            </form>


            <p
                style="
                    text-align:center;
                    margin-top:25px;
                "
            >

                Already have an account?

                <a href="/login">
                    Login
                </a>

            </p>


        </div>

    </div>

    """


# =========================================================
# LOGIN
# CORE FUNCTION 2
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        password = request.form["password"]


        resident = Resident.query.filter_by(
            email=email
        ).first()


        # -------------------------------
        # CHECK LOGIN
        # -------------------------------

        if resident and check_password_hash(
            resident.password,
            password
        ):

            session["resident_id"] = resident.id

            session["resident_name"] = resident.name

            return redirect("/dashboard")


        return STYLE + """

        <div class="container">

            <div class="card">

                <div class="error">

                    <strong>
                        Login Failed
                    </strong>

                    <br><br>

                    Invalid email or password.

                </div>


                <a
                    class="btn full-btn"
                    href="/login"
                >
                    Try Again
                </a>

            </div>

        </div>

        """


    # =====================================================
    # LOGIN FORM
    # =====================================================

    return STYLE + """

    <div class="navbar">

        <div class="logo">
            Smart Society
        </div>

    </div>


    <div class="container">

        <div class="card">

            <h2>
                Resident Login
            </h2>


            <form method="POST">


                <label>
                    Email Address
                </label>

                <input
                    type="email"
                    name="email"
                    required
                    placeholder="Enter your email"
                >


                <label>
                    Password
                </label>

                <input
                    type="password"
                    name="password"
                    required
                    placeholder="Enter your password"
                >


                <button
                    class="btn full-btn"
                    type="submit"
                >
                    Sign In
                </button>


            </form>


            <p
                style="
                    text-align:center;
                    margin-top:25px;
                "
            >

                New resident?

                <a href="/register">
                    Create an account
                </a>

            </p>


        </div>

    </div>

    """


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "resident_id" not in session:

        return redirect("/login")


    resident = db.session.get(
        Resident,
        session["resident_id"]
    )


    return STYLE + f"""

    <div class="navbar">

        <div class="logo">
            Smart Society
        </div>

        <div>

            <a
                href="/logout"
                style="
                    color:white;
                    text-decoration:none;
                "
            >
                Logout
            </a>

        </div>

    </div>


    <div class="container">


        <div class="dashboard-header">

            <h1>
                Welcome, {resident.name}
            </h1>

            <p>
                Resident | Flat No:
                {resident.flat_no}
            </p>

        </div>


        <h2>
            Resident Services
        </h2>


        <div class="features">


            <div class="module">

                <div class="module-icon">
                    📝
                </div>

                <h3>
                    Complaint Management
                </h3>

                <p>
                    Raise and track apartment
                    complaints.
                </p>

            </div>


            <div class="module">

                <div class="module-icon">
                    👥
                </div>

                <h3>
                    Visitor Management
                </h3>

                <p>
                    Manage visitor details and
                    visit records.
                </p>

            </div>


            <div class="module">

                <div class="module-icon">
                    💳
                </div>

                <h3>
                    Maintenance
                </h3>

                <p>
                    View maintenance bills and
                    payment status.
                </p>

            </div>


        </div>


    </div>


    <div class="footer">

        Smart Society |
        Resident Dashboard

    </div>

    """


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()


    return STYLE + """

    <div class="container">

        <div class="card">

            <div class="success">

                <strong>
                    Logged Out Successfully
                </strong>

                <br><br>

                Thank you for using
                Smart Society.

            </div>


            <a
                class="btn full-btn"
                href="/login"
            >
                Login Again
            </a>

        </div>

    </div>

    """


# =========================================================
# CREATE DATABASE
# =========================================================

with app.app_context():

    db.create_all()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)