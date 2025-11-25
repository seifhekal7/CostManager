# CostManager – Django REST API

CostManager is a backend service for managing personal expenses, categories, and monthly budgets.  
The system is built using Django REST Framework and secured with JWT authentication (SimpleJWT).

This documentation outlines the purpose, structure, installation process, environment configuration, and API endpoints of the project.

---

## Overview

CostManager enables each authenticated user to:

- Manage expense categories
- Record and modify expenses
- Create and track monthly budgets
- View calculated spending and remaining budget amounts
- Authenticate via JWT (Register, Login, Logout)

The application enforces strict data isolation, ensuring users can access only their own data.

---

## Features

### Authentication (JWT)
- User registration
- User login with access and refresh tokens
- Token blacklisting on logout
- All core endpoints require authentication

### Expense Management
- Create, update, delete, and retrieve expenses
- Automatic filtering by user
- Each expense linked to a category and user

### Budget Management
- Create a budget per month and category
- Automatic calculation of:
  - Total spent in a given month
  - Remaining amount

### Category Management
- User-specific categories
- CRUD operations for categories
- Automatic user data isolation

---

## Project Structure

```
project_root/
│
├── accounts/
│   ├── serializers.py
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── ...
││
├── costmanager/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── expense/
│   ├── serializers.py
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── ...
├── manage.py
├── Pipfile / requirements.txt
├── .env
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/CostManager.git
cd CostManager
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scriptsctivate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

or using Pipenv:

```bash
pipenv install
pipenv shell
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

---

## Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your_generated_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=1
TIME_ZONE=Africa/Cairo
```

Ensure `.env` is included in `.gitignore`.

---

## Authentication Endpoints

| Method | Endpoint        | Description |
|--------|----------------|-------------|
| POST   | /api/auth/register/ | Register a new user |
| POST   | /api/auth/login/    | Authenticate user and return tokens |
| POST   | /api/auth/logout/   | Blacklist the refresh token |

---

## API Endpoints

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/categories/ | List all categories for the user |
| POST   | /api/categories/ | Create a new category |
| GET    | /api/categories/<id>/ | Retrieve a category |
| PUT    | /api/categories/<id>/ | Update a category |
| DELETE | /api/categories/<id>/ | Delete a category |

### Expenses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/expenses/ | List user expenses |
| POST   | /api/expenses/ | Create a new expense |
| GET    | /api/expenses/<id>/ | Retrieve expense details |
| PUT    | /api/expenses/<id>/ | Update an expense |
| DELETE | /api/expenses/<id>/ | Delete an expense |

### Budgets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/budgets/ | List user budgets |
| POST   | /api/budgets/ | Create a new budget |
| GET    | /api/budgets/<id>/ | Retrieve a budget |
| PUT    | /api/budgets/<id>/ | Update a budget |
| DELETE | /api/budgets/<id>/ | Delete a budget |

---

## Key Technical Notes

### User-Based Query Filtering
All list and detail views filter objects by:
```python
queryset.filter(user=request.user)
```

### User Assignment on Creation
Each object created via POST automatically assigns the authenticated user:
```python
serializer.save(user=request.user)
```

### Budget Validation
The system validates monthly spending:
- Sums all expenses for the selected month

---

## License

This project may be used and modified freely unless otherwise specified.

---

## Developer

Seif Hekal 
Linkedin: www.linkedin.com/in/seifhekal7
Email: seifhekal7@gmail.com
