# InternHub — College Internship Management System

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/Database-MySQL-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Academic-purple.svg)]()

A centralized, responsive web platform designed to streamline and modernize the internship application, review, and tracking process for college students and academic placement coordinators.

---

## 🎓 Academic Details

- **Project Title**: InternHub — College Internship Management System
- **Candidate Name**: Hisana Hamza (Register No: MEA25MCA-2010)
- **Degree**: Master of Computer Applications (MCA)
- **Institution**: Department of Computer Applications, MEA Engineering College, Perinthalmanna
- **University**: APJ Abdul Kalam Technological University, Kerala

---

## 📌 Abstract & Overview

Traditional college internship tracking often relies on disconnected Google Forms, manual spreadsheets, email threads, and social media notices. This fragmentation leads to missed deadlines, lack of transparency, manual tracking overhead, and communication gaps between students and administrators.

**InternHub** resolves these challenges by providing:
1. **Centralized Student Portal**: Secure account registration, authentication, and customizable profile management.
2. **Curated Internship Discovery**: Search and filter opportunities across technical domains, locations, and stipends with clear deadline warnings.
3. **1-Click Application Flow**: Submit applications with automated duplicate detection and optional pending-application withdrawal.
4. **Interactive Dashboard & Metrics**: Real-time analytics tracking applications across *Pending*, *Under Review*, *Shortlisted*, *Selected*, and *Rejected* lifecycles.
5. **Real-Time Notification Dispatch**: Immediate alerts whenever an administrator updates an application's review status.
6. **Administrator Control Center**: Customized Django Admin panel with bulk status transition actions and audit trails.

---

## 🏗 System Architecture & Database Design

### Database Tables & Schema

1. **`user_management_student`**:
   - `id` (Primary Key, INT)
   - `user_id` (OneToOneField -> `auth_user`, CASCADE)
   - `name` (VARCHAR 100, Full Name)
   - `email` (EmailField)
   - `phone` (VARCHAR 15)
   - `course` (VARCHAR 100, e.g. MCA, B.Tech CSE, BCA)
   - `created_at` (DateTimeField)

2. **`internships_internship`**:
   - `id` (Primary Key, INT)
   - `title` (VARCHAR 200, Role Title)
   - `company_name` (VARCHAR 200)
   - `description` (TEXT)
   - `location` (VARCHAR 100)
   - `duration` (VARCHAR 100)
   - `stipend` (VARCHAR 100)
   - `skills_required` (VARCHAR 300, comma-separated tags)
   - `application_deadline` (DateField)
   - `created_at` (DateTimeField)

3. **`internships_application`**:
   - `id` (Primary Key, INT)
   - `student_id` (ForeignKey -> `Student`, CASCADE)
   - `internship_id` (ForeignKey -> `Internship`, CASCADE)
   - `applied_at` (DateTimeField)
   - `status` (VARCHAR 20, Choices: *Pending*, *Under Review*, *Shortlisted*, *Selected*, *Rejected*)
   - *Constraint*: `unique_student_internship_application` (ensures single application per role)

4. **`internships_notification`**:
   - `id` (Primary Key, INT)
   - `student_id` (ForeignKey -> `Student`, CASCADE)
   - `message` (TEXT)
   - `is_read` (BOOLEAN, Default: False)
   - `created_at` (DateTimeField)

---

## 🎨 UI/UX Design System

- **Color Palette**:
  - Primary Navy: `#1F3C88` (Brand Blue)
  - Accent Electric Blue: `#2563EB`
  - Deep Slate: `#0F172A`
  - Soft Canvas: `#F4F7FB`
- **Status Indicators**:
  - ⏳ **Pending**: Warm Amber (`#D97706` / `#FEF3C7`)
  - 🔍 **Under Review**: Electric Blue (`#2563EB` / `#DBEAFE`)
  - ⭐ **Shortlisted**: Royal Purple (`#7C3AED` / `#EDE9FE`)
  - 🎉 **Selected**: Emerald Green (`#059669` / `#D1FAE5`)
  - ✕ **Rejected**: Rose Crimson (`#E11D48` / `#FFE4E6`)
- **Responsive Architecture**: Mobile hamburger menu, flexible CSS grid cards, and sticky navigation bar.

---

## ⚙️ Installation & Setup Guide

### 1. Prerequisites
- Python 3.9+ installed
- MySQL Server running (default port 3307 or 3306)

### 2. Clone or Open Project
```powershell
cd c:\Users\hisan\OneDrive\Documents\Project\InternHub
```

### 3. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Configure Database
Ensure MySQL database `internhub` exists:
```sql
CREATE DATABASE internhub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
Check `config/settings.py` for your database credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'internhub',
        'USER': 'root',
        'PASSWORD': 'YourNewPassword',
        'HOST': 'localhost',
        'PORT': '3307',
    }
}
```

### 5. Apply Migrations
```powershell
python manage.py migrate
```

### 6. Seed Sample Internship Postings
Populate verified technical internships across domains:
```powershell
python manage.py seed_data
```

### 7. Create Superuser (Admin Access)
```powershell
python manage.py createsuperuser
```

### 8. Run Development Server
```powershell
python manage.py runserver
```
Access the application at:
- **Student & Public Portal**: http://127.0.0.1:8000/
- **Admin Management Portal**: http://127.0.0.1:8000/admin/

---

## 🧪 Automated Testing

Execute the test suite covering registration, authentication, profile updates, internship filtering, application duplicate checks, deadline validation, withdrawal, and admin bulk actions:
```powershell
python manage.py test
```

---

## 👥 User Roles & Permissions

| Role | Access | Key Capabilities |
|------|--------|------------------|
| **Guest** | `/`, `/internships/` | Browse opportunities, search roles, view requirements, register/login |
| **Student** | `/dashboard/`, `/profile/`, `/my_applications/`, `/notifications/` | Apply for internships, withdraw pending applications, track live status, update profile |
| **Administrator** | `/admin/`, `/students/` | Post/manage internships, review student submissions, bulk status updates with automated notification triggers |

---

## 📄 License & Acknowledgments

Developed as part of the MCA curriculum for APJ Abdul Kalam Technological University at MEA Engineering College.
Supervised by Adil Narakkoden (Assistant Professor & Project Guide) and Sajeesh M (Head of Department).
