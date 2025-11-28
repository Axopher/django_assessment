# Project Setup Guide

This document explains how to set up the Django project using either a Python virtual environment or Docker, and provides a step-by-step guide to testing the API using Postman.

---

## 🔧 Prerequisites

Make sure you have the following installed:

- **Python 3.12+**
- **Docker** (Recommended for running PostgreSQL easily)
- **Git**

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Axopher/django_assessment.git
cd django_assessment
```

### 2. Create environment config

```bash
cp .env.example .env
```

# ⚙️ Installation Methods

Choose one of the following methods to run the application.

## Option A: Docker Setup (Recommended)

```bash
# Build and run containers
docker compose up --build -d

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser
```

---

## Option B: Python Virtual Environment Setup

Note: Ensure you have PostgreSQL installed and running on your local machine before proceeding.

```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate       # macOS/Linux
# venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations and setup
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 👤 Superuser Credentials

During the `createsuperuser` process, use the following values to ensure the testing flow works correctly:

| Field        | Value             |
| :----------- | :---------------- |
| **Username** | `admin`           |
| **Email**    | `admin@gmail.com` |
| **Role**     | `SUPER_ADMIN`     |
| **Country**  | `GLOBAL`          |
| **Password** | `<yourpassword>`  |

---

## 🧪 API Testing Guide

### 1. Postman Setup

Open Postman and import the collection using this URL:

```
Link in the email.
```

## Test 1: Authentication & Roles (JWT Tokens)

### A. Obtain Tokens (Login)

#### Endpoint: POST /api/token/

#### Body: {"username": "admin", "password": "yourpassword"}

#### Expected: Success (Status 200). You receive access and refresh tokens.

### B. Attempt Unauthorized Creation (Test RBAC)

#### Endpoint: POST /api/users/register/

#### Header: No Authorization Header

#### Expected: Failure (Status 401 Unauthorized). All views require authentication.

## Test 2: Enforcing Role-Based Access Control (RBAC)

### A. Super Admin Creation Use the Super Admin's token for these requests.

#### Create Country Admin

#### Endpoint: POST /api/users/register/

#### Body:

```JSON
{
"username": "ca_us",
"email": "ca_us@g.com",
"password": "pass",
"role": "COUNTRY_ADMIN",
"country": "USA"
}
```

#### Expected: Success (Status 201). Super Admin can create any role/country.

---

#### Create Country Member

#### Body:

```JSON

{
"username": "cm_uk",
"email": "cm_uk@g.com",
"password": "pass",
"role": "COUNTRY_MEMBER",
"country": "UK"
}
```

#### Expected: Success (Status 201).

### B. Country Admin Creation

Login as the Country Admin (ca_us) created above to get a new token.

### Valid Creation (Member in Own Country)

#### Endpoint: POST /api/users/register/

#### Body:

```JSON
{
  "username": "cm_us",
  "email": "cm_us@g.com",
  "password": "pass",
  "role": "COUNTRY_MEMBER",
  "country": "USA"
}
```

#### Expected: Success (Status 201). Passes RBAC.

---

### Invalid Creation (Wrong Country)

#### Body:

```
{ ..., "country": "Canada" }
```

#### Expected: Failure (Status 403 Forbidden). Fails RBAC.

---

### Invalid Creation (Higher Role)

#### Body:

```
{ ..., "role": "COUNTRY_ADMIN" }
```

#### Expected: Failure (Status 403 Forbidden). Fails RBAC (Cannot create same or higher level role).

---

## Test 3: Sample CRUD Feature (Projects)

Use the Super Admin token.

### A. Create Project

#### Endpoint: POST /api/projects/

#### Body:

```
{"title": "First Project", "description": "Audit Log Test", "status": "TODO"}
```

#### Expected: Success (Status 201). created_by should point to the Super Admin's ID.

### B. Update Project

#### Endpoint: PUT /api/projects/1/

#### Body:

```
{
   "title": "Updated Title",
   "description": "This triggered an audit log.",
   "status": "IN_PROGRESS"
}
```

#### Expected: Success (Status 200).

### C. Delete Project

#### Endpoint: DELETE /api/projects/1/

#### Expected: Success (Status 204 No Content).

---

## Test 4: Audit Logging

#### Verify the logged data via endpoint:

```
localhost:8000/admin
```

Login as super user.
