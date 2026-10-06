from flask import Flask, request, redirect, session, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from ai_engine import analyze_complaint

app = Flask(__name__)
app.secret_key = "smart"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        BASE_DIR,
        "instance",
        "smart_society.db"
    )

db = SQLAlchemy(app)


class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    flat_no = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer)
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    status = db.Column(db.String(30), default="Pending")


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer)
    visitor_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    visit_date = db.Column(db.String(20))
    purpose = db.Column(db.String(150))


class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer)
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    status = db.Column(db.String(30), default="Pending")


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "application": "Smart Society Apartment Management Platform"
    }


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form["email"].lower()

        if Resident.query.filter_by(email=email).first():
            return "Email already registered. Please login."

        resident = Resident(
            name=request.form["name"],
            flat_no=request.form["flat_no"],
            phone=request.form["phone"],
            email=email,
            password=generate_password_hash(
                request.form["password"]
            )
        )

        db.session.add(resident)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        resident = Resident.query.filter_by(
            email=request.form["email"].lower()
        ).first()

        if resident and check_password_hash(
            resident.password,
            request.form["password"]
        ):

            session.clear()

            session["type"] = "resident"
            session["id"] = resident.id
            session["resident_name"] = resident.name

            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if session.get("type") != "resident":
        return redirect("/login")

    return render_template("dashboard.html")


@app.route("/complaints", methods=["GET", "POST"])
def complaints():

    if session.get("type") != "resident":
        return redirect("/login")

    if request.method == "POST":

        complaint = Complaint(
            resident_id=session["id"],
            title=request.form["title"],
            description=request.form["description"]
        )

        db.session.add(complaint)
        db.session.commit()

    complaints = Complaint.query.filter_by(
        resident_id=session["id"]
    ).all()

    return render_template(
        "complaints.html",
        complaints=complaints
    )


@app.route("/visitors", methods=["GET", "POST"])
def visitors():

    if session.get("type") != "resident":
        return redirect("/login")

    if request.method == "POST":

        visitor = Visitor(
            resident_id=session["id"],
            visitor_name=request.form["visitor_name"],
            phone=request.form["phone"],
            visit_date=request.form["visit_date"],
            purpose=request.form["purpose"]
        )

        db.session.add(visitor)
        db.session.commit()

    visitors = Visitor.query.filter_by(
        resident_id=session["id"]
    ).all()

    return render_template(
        "visitors.html",
        visitors=visitors
    )


@app.route("/visitors/delete/<int:id>", methods=["POST"])
def delete_visitor(id):

    if session.get("type") != "resident":
        return redirect("/login")

    visitor = Visitor.query.get_or_404(id)

    if visitor.resident_id == session["id"]:

        db.session.delete(visitor)
        db.session.commit()

    return redirect("/visitors")


@app.route("/maintenance", methods=["GET", "POST"])
def maintenance():

    if session.get("type") != "resident":
        return redirect("/login")

    if request.method == "POST":

        maintenance_request = Maintenance(
            resident_id=session["id"],
            title=request.form["title"],
            description=request.form["description"]
        )

        db.session.add(maintenance_request)
        db.session.commit()

    requests = Maintenance.query.filter_by(
        resident_id=session["id"]
    ).all()

    return render_template(
        "maintenance.html",
        requests=requests
    )


@app.route("/maintenance/delete/<int:id>", methods=["POST"])
def delete_maintenance(id):

    if session.get("type") != "resident":
        return redirect("/login")

    maintenance_request = Maintenance.query.get_or_404(id)

    if maintenance_request.resident_id == session["id"]:

        db.session.delete(maintenance_request)
        db.session.commit()

    return redirect("/maintenance")


@app.route("/profile")
def profile():

    if session.get("type") != "resident":
        return redirect("/login")

    resident = Resident.query.get(session["id"])

    return render_template(
        "profile.html",
        resident=resident
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        admin = Admin.query.filter_by(
            email=request.form["email"].lower()
        ).first()

        if admin and check_password_hash(
            admin.password,
            request.form["password"]
        ):

            session.clear()
            session["type"] = "admin"

            return redirect("/admin/dashboard")

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():

    if session.get("type") != "admin":
        return redirect("/admin/login")

    total_residents = Resident.query.count()

    total_complaints = Complaint.query.count()

    pending = Complaint.query.filter_by(
        status="Pending"
    ).count()

    resolved = Complaint.query.filter_by(
        status="Resolved"
    ).count()

    complaints = Complaint.query.all()

    critical = 0
    high = 0
    medium = 0
    low = 0

    categories = {}

    priority_complaints = []

    for complaint in complaints:

        text = complaint.title + " " + complaint.description

        ai = analyze_complaint(text)

        risk = ai["risk"]
        category = ai["category"]

        if risk == "Critical":
            critical += 1

        elif risk == "High":
            high += 1

        elif risk == "Medium":
            medium += 1

        elif risk == "Low":
            low += 1

        categories[category] = categories.get(
            category,
            0
        ) + 1

        if complaint.status != "Resolved":

            priority_complaints.append({
                "title": complaint.title,
                "risk": ai["risk"],
                "risk_score": ai["risk_score"],
                "category": ai["category"],
                "recommendation": ai["recommendation"]
            })

    priority_complaints.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    most_common_category = "No Data"

    if categories:

        most_common_category = max(
            categories,
            key=categories.get
        )

    return render_template(
        "admin_dashboard.html",
        total_residents=total_residents,
        total_complaints=total_complaints,
        pending=pending,
        resolved=resolved,
        critical=critical,
        high=high,
        medium=medium,
        low=low,
        most_common_category=most_common_category,
        priority_complaints=priority_complaints[:3]
    )


@app.route(
    "/admin/complaints",
    methods=["GET", "POST"]
)
def admin_complaints():

    if session.get("type") != "admin":
        return redirect("/admin/login")

    if request.method == "POST":

        complaint = Complaint.query.get(
            request.form["id"]
        )

        if complaint:

            complaint.status = request.form["status"]

            db.session.commit()

    complaints = Complaint.query.all()

    ai_results = {}

    for complaint in complaints:

        text = complaint.title + " " + complaint.description

        ai_results[complaint.id] = analyze_complaint(text)

    return render_template(
        "admin_complaints.html",
        complaints=complaints,
        ai_results=ai_results
    )


@app.route("/admin/complaints/<status>")
def complaint_status(status):

    if session.get("type") != "admin":
        return redirect("/admin/login")

    if status not in ["Pending", "Resolved"]:
        return redirect("/admin/complaints")

    complaints = Complaint.query.filter_by(
        status=status
    ).all()

    ai_results = {}

    for complaint in complaints:

        text = complaint.title + " " + complaint.description

        ai_results[complaint.id] = analyze_complaint(text)

    return render_template(
        "admin_complaints.html",
        complaints=complaints,
        ai_results=ai_results
    )


@app.route("/admin/residents")
def admin_residents():

    if session.get("type") != "admin":
        return redirect("/admin/login")

    residents = Resident.query.all()

    return render_template(
        "admin_residents.html",
        residents=residents
    )


@app.route(
    "/admin/resident/delete/<int:id>",
    methods=["POST"]
)
def delete_resident(id):

    if session.get("type") != "admin":
        return redirect("/admin/login")

    resident = Resident.query.get_or_404(id)

    db.session.delete(resident)
    db.session.commit()

    return redirect("/admin/residents")


@app.route("/admin/visitors")
def admin_visitors():

    if session.get("type") != "admin":
        return redirect("/admin/login")

    visitors = Visitor.query.all()

    return render_template(
        "admin_visitors.html",
        visitors=visitors
    )


@app.route("/admin/maintenance")
def admin_maintenance():

    if session.get("type") != "admin":
        return redirect("/admin/login")

    requests = Maintenance.query.all()

    return render_template(
        "admin_maintenance.html",
        requests=requests
    )


@app.route(
    "/admin/maintenance/update",
    methods=["POST"]
)
def update_maintenance():

    if session.get("type") != "admin":
        return redirect("/admin/login")

    request_id = request.form["id"]

    new_status = request.form["status"]

    maintenance_request = Maintenance.query.get_or_404(
        request_id
    )

    if new_status in [
        "Pending",
        "In Progress",
        "Resolved"
    ]:

        maintenance_request.status = new_status

        db.session.commit()

    return redirect("/admin/maintenance")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


with app.app_context():

    os.makedirs(
        os.path.join(BASE_DIR, "instance"),
        exist_ok=True
    )

    db.create_all()

    if not Admin.query.filter_by(
        email="admin@smartsociety.com"
    ).first():

        admin = Admin(
            email="admin@smartsociety.com",
            password=generate_password_hash(
                "admin123"
            )
        )

        db.session.add(admin)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)