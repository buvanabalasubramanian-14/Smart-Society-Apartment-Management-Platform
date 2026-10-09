Smart Society Apartment Management Platform

A full-stack, multi-user apartment management platform that helps residents and administrators manage society services, complaints, visitors, and maintenance requests through a web application. The platform also includes AI-assisted complaint analysis and priority alerts to support administrative decision-making.

Table of Contents

- "Overview" (#overview)
- "Features" (#features)
- "AI-Powered Complaint Analysis" (#ai-powered-complaint-analysis)
- "User Roles" (#user-roles)
- "Technology Stack" (#technology-stack)
- "Database Modules" (#database-modules)
- "System Design Documentation" (#system-design-documentation)
- "Project Structure" (#project-structure)
- "System Flow" (#system-flow)
- "Testing" (#testing)
- "CI/CD" (#cicd)
- "Security" (#security)
- "Cloud Deployment" (#cloud-deployment)
- "Local Setup" (#local-setup)
- "Admin Login" (#admin-login)
- "Future Enhancements" (#future-enhancements)
- "Author" (#author)

Overview

The Smart Society Apartment Management Platform provides separate resident and administrator workflows. Residents can register, sign in, submit complaints, manage visitor details, and view maintenance information. Administrators can review resident records, manage complaints, update statuses, and manage visitor and maintenance records.

The application is designed as a multi-user system with role-based access to resident and admin functionality.

Features

Resident Module

- Resident registration
- Secure resident login and logout
- Resident dashboard
- Complaint registration
- Complaint status tracking
- Visitor management
- Maintenance request management
- Resident profile

Admin Module

- Separate admin login portal
- Admin dashboard and statistics
- View and manage registered residents
- View resident complaints
- Update complaint status
- View and manage visitor records
- View maintenance requests
- Update maintenance status
- Resident deletion management

Platform Features

- Role-based access to protected routes
- Database-backed society records
- AI-assisted complaint analysis and priority alerts
- Automated tests and code-quality checks
- Cloud deployment using Render

AI-Powered Complaint Analysis

The application includes AI-assisted complaint analysis to help administrators review resident complaints and identify those that may need earlier attention.

- AI-assisted complaint analysis
- Complaint priority alerts
- Analysis integrated into the complaint-management workflow
- Decision-support information for administrators

AI-generated analysis is intended to support—not replace—administrator review. Administrators remain responsible for verifying complaint details and deciding what action to take.

User Roles

Resident

Residents can:

- Create an account and sign in
- View their dashboard
- Register complaints and track their status
- Add and manage visitor details
- Submit or view maintenance information
- View their profile
- Log out securely

Admin

Administrators can:

- Sign in through the admin portal
- View dashboard statistics
- View and manage resident records
- Review complaints and update their statuses
- View visitor records
- Review maintenance requests and update statuses
- Use AI-assisted complaint analysis and priority alerts where available

Technology Stack

Component| Technology
Frontend| HTML, CSS, Jinja Templates
Backend| Python, Flask
Database| PostgreSQL in cloud deployment / SQLite for local development, as configured
ORM| Flask-SQLAlchemy
Authentication| Session-based authentication
Password Security| Werkzeug password hashing
Testing| Pytest
Code Quality| Flake8
Deployment| Render
CI/CD| GitHub Actions
Production Server| Gunicorn

Database Modules

The main database entities are:

- Resident — resident profile and account information
- Admin — administrator account information
- Complaint — complaint details, status, date, and associated resident
- Visitor — visitor details and associated resident
- Maintenance — maintenance amount, due date, payment status, and associated resident

The exact fields and relationships are defined by the application's database models.

System Design Documentation

The "docs/" directory contains project design documentation, including:

- Software Architecture Diagram
- Entity Relationship (ER) Diagram

The architecture diagram describes the main application components and their interactions. The ER diagram documents the database entities, primary keys, foreign keys, and resident-related one-to-many relationships.

Refer to the "docs/" folder for the diagrams.

Project Structure

Smart-Society-Apartment-Management-Platform/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   │   └── style.css
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
│   └── instance/
├── tests/
│   └── test_app.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
├── .gitignore
├── README.md
└── CHANGELOG.md

This structure is representative. Keep the actual repository structure as the source of truth if filenames differ.

System Flow

Home Page
   |
   v
Resident Login / Registration  or  Admin Login
   |
   v
Authentication and Role-Based Access
   |
   v
Resident Dashboard / Admin Dashboard
   |
   +--> Complaint Management
   |       |
   |       +--> AI-Assisted Complaint Analysis / Priority Alerts
   |
   +--> Visitor Management
   |
   +--> Maintenance Management
   |
   v
Database

Testing

The project uses Pytest for automated testing. The documented test areas include:

- Health endpoint
- Home page
- Login page
- Registration page
- Admin login page
- Protected resident routes
- Protected admin routes
- Complaint route protection
- Visitor route protection
- Maintenance route protection

Run the test suite after installing the required dependencies:

pytest

If your test configuration requires a particular directory or environment variables, follow the project's current test configuration.

CI/CD

GitHub Actions is used for continuous integration. The documented workflow performs these steps:

1. Checks out the source code.
2. Sets up Python.
3. Installs dependencies.
4. Runs Flake8 code-quality checks.
5. Runs Pytest tests.

Changes pushed to the configured branch can trigger the workflow. Deployment behavior depends on the Render and GitHub integration settings configured for the repository.

Security

The application documentation includes the following security measures:

- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control
- Protected dashboard routes
- Server-side validation
- ORM-based database operations
- Environment-based database configuration
- Sensitive configuration stored in deployment environment variables

Do not commit real passwords, API keys, database URLs containing credentials, or other secrets to the public repository. Configure production secrets through the hosting provider's environment settings.

Cloud Deployment

The application is hosted on Render.

- Live Application: https://smart-society-apartment-management.onrender.com/
- GitHub Repository: https://github.com/buvanabalasubramanian-14/Smart-Society-Apartment-Management-Platform

Production Components

- Web application hosting: Render
- Production server: Gunicorn
- Cloud database: PostgreSQL, if configured for the deployed environment
- Source code: GitHub
- Continuous integration: GitHub Actions

After deployment, verify the live application by testing resident login, admin login, complaint submission, AI-assisted analysis and priority alerts, visitor management, and maintenance workflows.

Local Setup

Prerequisites

- Python installed
- Git
- A code editor such as Visual Studio Code

1. Clone the Repository

git clone https://github.com/buvanabalasubramanian-14/Smart-Society-Apartment-Management-Platform.git
cd Smart-Society-Apartment-Management-Platform

2. Create and Activate a Virtual Environment

Windows PowerShell:

python -m venv venv
.\venv\Scripts\Activate.ps1

3. Install Dependencies

pip install -r backend/requirements.txt

4. Configure Environment Variables

Set any required configuration values in your local environment. Do not commit secrets. Database configuration should match the settings expected by "backend/app.py".

5. Run the Application

cd backend
python app.py

6. Open the Application

Visit:

http://127.0.0.1:5000

Admin Login

The application provides a separate admin login portal for society management.

Configure administrator credentials using the application's supported configuration method. Do not store sensitive admin passwords in this public README or commit them to the repository.

Future Enhancements

- Online maintenance payments
- Notifications
- Expanded complaint-priority management
- Reports and analytics
- Email/SMS notifications
- Advanced visitor approval
- Society announcements

Author

Buvana Balasubramanian

Project Type: Full-Stack Web Application | Multi-User Apartment Management Systems