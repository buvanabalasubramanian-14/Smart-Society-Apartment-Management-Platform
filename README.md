# Smart Society Apartment Management Platform

A full-stack web-based apartment management platform designed to help residents and administrators manage apartment society services efficiently.

## Features

### Resident Module

- Resident Registration
- Secure Resident Login
- Resident Dashboard
- Complaint Registration
- Complaint Status Tracking
- Visitor Management
- Maintenance Request Management
- Resident Profile
- Logout

### Admin Module

- Admin Login
- Admin Dashboard
- Resident Management
- View and Manage Complaints
- Update Complaint Status
- Visitor Management
- Maintenance Management
- Update Maintenance Status
- Resident Delete Management

## User Roles

### Resident

Residents can:

- Create an account
- Login securely
- View dashboard
- Register complaints
- Track complaint status
- Add and manage visitors
- Submit maintenance requests
- View profile

### Admin

Administrators can:

- Login through the admin portal
- View dashboard statistics
- View registered residents
- Manage residents
- View resident complaints
- Update complaint status
- View visitors
- View maintenance requests
- Update maintenance status

## Technology Stack

- Frontend: HTML, CSS, Jinja Templates
- Backend: Python Flask
- Database: PostgreSQL (Cloud) / SQLite (Local Development)
- ORM: Flask-SQLAlchemy
- Authentication: Session-based Authentication
- Password Security: Werkzeug Password Hashing
- Testing: Pytest
- Code Quality: Flake8
- Deployment: Render
- CI/CD: GitHub Actions
- Production Server: Gunicorn

## Database Modules

The application contains the following main database tables:

- Resident
- Admin
- Complaint
- Visitor
- Maintenance

The database stores resident information, complaints, visitor details and maintenance requests.

## Project Structure

```text
Smart-Society-Apartment-Management-Platform/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   │   └── style.css
│   │
│   ├── templates/
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── complaints.html
│   │   ├── visitors.html
│   │   ├── maintenance.html
│   │   ├── profile.html
│   │   ├── admin_login.html
│   │   ├── admin_dashboard.html
│   │   ├── admin_complaints.html
│   │   ├── admin_residents.html
│   │   ├── admin_visitors.html
│   │   └── admin_maintenance.html
│   │
│   └── instance/
│
├── tests/
│   └── test_app.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
├── .gitignore
├── README.md
└── CHANGELOG.md

System Flow
Home
  ↓
Resident / Admin Login
  ↓
Authentication
  ↓
Role-Based Dashboard
  ↓
Society Services
  ↓
Complaint Management
  ↓
Visitor Management
  ↓
Maintenance Management
  ↓
Database

Testing
The project uses Pytest for automated testing.
Current tests cover:
Health endpoint
Home page
Login page
Registration page
Admin login page
Protected resident routes
Protected admin routes
Complaint route protection
Visitor route protection
Maintenance route protection
Run tests using:
    pytest


CI/CD
GitHub Actions is used for continuous integration.
The workflow performs:
Checkout source code
Setup Python
Install dependencies
Run Flake8 linting
Run Pytest tests
The application is connected to GitHub and changes pushed to the main branch trigger the deployment workflow.

Security
The application includes:
Password hashing
Session-based authentication
Role-based access control
Protected dashboard routes
Server-side validation
ORM-based database operations
Environment-based database configuration
Sensitive database configuration is stored using environment variables in the cloud deployment environment.

Cloud Deployment
The application is deployed using Render.

Production Components
Web Application: Render
Production Server: Gunicorn
Cloud Database: PostgreSQL
Source Code: GitHub
Continuous Integration: GitHub Actions

Live Application
     https://smart-society-apartment-management.onrender.com/

GitHub Repository
Repository:
https://github.com/buvanabalasubramanian-14/Smart-Society-Apartment-Management-Platform⁠�

Local Setup

1. Create virtual environment
python -m venv venv

2. Activate virtual environment
Windows:
venv\Scripts\activate

3. Install dependencies
pip install -r backend/requirements.txt

4. Run the application
cd backend
python app.py

5. Open in browser
http://127.0.0.1:5000

Admin Login

The application provides a separate admin login portal for society management.

Admin credentials should be configured securely and should not be stored as sensitive information in the public repository.

Project Type
Full-Stack Web Application | Multi-User Apartment Management System

Future Enhancements
   Online Maintenance Payment
   Notifications
   Complaint Priority Management
   Reports and Analytics
   Email/SMS Notifications
   Advanced Visitor Approval
   Society Announcements


Author
Buvana Balasubramanian