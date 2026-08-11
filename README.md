Smart Society Apartment Management Platform

A web-based apartment management platform that helps residents and administrators manage society services efficiently.

Features

Resident Module
- Resident Registration
- Secure Resident Login
- Resident Dashboard
- Complaint Registration
- Complaint Status Tracking
- Resident Profile

Admin Module
- Admin Login
- Admin Dashboard
- View Resident Complaints
- Manage Complaint Status

User Roles

- **Resident** – Register, login, submit complaints and track complaints.
- **Admin** – Login, view complaints and manage complaint status.

Technology Stack

- Frontend: HTML, CSS
- Backend: Python Flask
- Database: SQLite
- ORM: Flask-SQLAlchemy
- Authentication: Session-based Login
- Password Security: Werkzeug Password Hashing

Project Structure

text
Smart-Society-Apartment-Management-Platform/
│
├── backend/
│   ├── app.py
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── complaints.html
│   │   ├── admin_login.html
│   │   ├── admin_dashboard.html
│   │   └── admin_complaints.html
│   └── instance/
│
├── docs/
├── .gitignore
└── README.md

How to Run

1. Create virtual environment
python -m venv venv

2. Activate environment
Windows:
venv\Scripts\activate

3. Install dependencies
pip install flask flask-sqlalchemy werkzeug

4. Run the application
cd backend
python app.py

5. Open in browser
http://127.0.0.1:5000

System Flow

Home
  ↓
Resident / Admin Login
  ↓
Authentication
  ↓
Dashboard
  ↓
Society Services
  ↓
Complaint Management
  ↓
Database


Database

       The application uses SQLite for storing resident and complaint information.
Database files are excluded from GitHub using .gitignore.


Security

       Password hashing
       Session-based authentication
       Role-based access
       Input validation
       Protected dashboard routes


Future Enhancements

       Visitor Management
       Maintenance Payment Management
       Notifications
       Admin Resident Management
       Complaint Priority Management
       Reports and Analytics


Project Type

        Full-Stack Web Application | Multi-User Apartment Management System


Author

Buvana Balasubramanian