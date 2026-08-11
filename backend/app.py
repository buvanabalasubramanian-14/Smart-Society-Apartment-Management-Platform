from flask import Flask,request,redirect,session,render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)
app.config["SECRET_KEY"]="smart"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///smart_society.db"
db=SQLAlchemy(app)

class Resident(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    flat_no=db.Column(db.String(20))
    phone=db.Column(db.String(20))
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(200))

class Admin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(200))

class Complaint(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    resident_id=db.Column(db.Integer)
    title=db.Column(db.String(150))
    description=db.Column(db.Text)
    status=db.Column(db.String(30),default="Pending")

@app.route("/")
def home(): return render_template("home.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        r=Resident(name=request.form["name"],flat_no=request.form["flat_no"],
        phone=request.form["phone"],email=request.form["email"].lower(),
        password=generate_password_hash(request.form["password"]))
        db.session.add(r);db.session.commit();return redirect("/login")
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        r=Resident.query.filter_by(email=request.form["email"].lower()).first()
        if r and check_password_hash(r.password,request.form["password"]):
            session.clear();session["type"]="resident";session["id"]=r.id
            session["resident_name"]=r.name;session["resident_email"]=r.email
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html") if session.get("type")=="resident" else redirect("/login")

@app.route("/complaints",methods=["GET","POST"])
def complaints():
    if session.get("type")!="resident": return redirect("/login")
    if request.method=="POST":
        db.session.add(Complaint(resident_id=session["id"],
        title=request.form["title"],description=request.form["description"]))
        db.session.commit()
    return render_template("complaints.html",
        complaints=Complaint.query.filter_by(resident_id=session["id"]).all())

@app.route("/admin/login",methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
        a=Admin.query.filter_by(email=request.form["email"].lower()).first()
        if a and check_password_hash(a.password,request.form["password"]):
            session.clear();session["type"]="admin";return redirect("/admin/dashboard")
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html") if session.get("type")=="admin" else redirect("/admin/login")

@app.route("/admin/complaints",methods=["GET","POST"])
def admin_complaints():
    if session.get("type")!="admin": return redirect("/admin/login")
    if request.method=="POST":
        c=Complaint.query.get(request.form["id"])
        if c:c.status=request.form["status"];db.session.commit()
    return render_template("admin_complaints.html",complaints=Complaint.query.all())

@app.route("/logout")
def logout(): session.clear();return redirect("/")

with app.app_context():
    db.create_all()
    if not Admin.query.filter_by(email="admin@smartsociety.com").first():
        db.session.add(Admin(email="admin@smartsociety.com",
        password=generate_password_hash("admin123")));db.session.commit()

if __name__=="__main__": app.run(debug=True)