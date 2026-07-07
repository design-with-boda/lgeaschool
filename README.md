# L.G.E.A STAFF SCHOOL, KEFFI NASARAWA STATE — Primary School Portal

A modern, responsive, and secure school management portal built with Django and Bootstrap 5.

## Features
- **Frontend:** Responsive homepage, about, academics, admission, gallery, news, events, contact.
- **Backend:** Full Django admin integration, role-based dashboards (Admin, Teacher, Student).
- **Student Management:** Profiles, attendance, results checking.
- **Teacher Management:** Profiles, subject assignment.
- **Academics:** Result processing (CA & Exam), learning materials.
- **Design:** Modern UI/UX styled with custom CSS matching Nigerian public education institutions.

## Setup Instructions

Since you are on Windows, follow these steps in your terminal (Command Prompt or PowerShell) within the project folder (`c:\Users\akal\Desktop\lgea web`):

### 1. Create a Virtual Environment (Recommended)
```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Apply Database Migrations
```powershell
python manage.py makemigrations core accounts students teachers academics news gallery
python manage.py migrate
```

### 4. Seed the Database with Demo Data
This command will create all demo students, teachers, subjects, events, announcements, and an Admin account.
```powershell
python manage.py seed_data
```

### 5. Run the Server
```powershell
python manage.py runserver
```

## Accessing the Portal
- **Main Website:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Dashboard:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Demo Credentials (created by `seed_data`)
- **Admin Login:** 
  - Username: `admin`
  - Password: `Admin@2025!`
