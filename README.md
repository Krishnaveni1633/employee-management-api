# 🏢 Employee Management System API

A production-ready Full Stack Employee Management System built with modern technologies.

## 🌍 Live Demo
- **API:** https://employee-management-api-59jd.onrender.com
- **API Docs:** https://employee-management-api-59jd.onrender.com/docs

## 📌 About
This is a complete Employee Management System that allows companies to digitally manage their employees with proper security, AI document summarization, and email notifications.

## 🚀 Tech Stack

### Backend
- **Python 3.13** — Programming language
- **FastAPI** — Modern, fast web framework
- **PostgreSQL** — Relational database
- **SQLAlchemy** — ORM for database operations
- **JWT** — Secure authentication
- **bcrypt** — Password hashing
- **Docker** — Containerization

### AI and Communication
- **Claude AI (Anthropic)** — Document summarization
- **FastAPI Mail** — Email notifications

### Frontend
- **React.js** — User interface
- **Axios** — API calls
- **React Router** — Navigation
- **React Toastify** — Notifications

### Deployment
- **Render.com** — Cloud deployment
- **Docker** — Container deployment

## Features

### Authentication and Security
- User registration with role assignment
- JWT token authentication
- bcrypt password hashing
- Role based access control (Admin/Manager/Employee)
- Protected API endpoints

### Employee Management
- Add new employees (Admin only)
- View all employees (Manager and above)
- Update employee details (Manager and above)
- Delete employees (Admin only)
- Search by name or email
- Filter by department
- Pagination support

### AI Document Summarizer
- Upload PDF documents
- AI powered text extraction
- Automatic document summarization using Claude AI
- Summary saved to database
- Summary emailed automatically

### Email Notifications
- Welcome email on registration
- Notification when new employee added
- Document summary emailed automatically

### Frontend
- Login page
- Dashboard with role display
- Employee list with search and filter
- Add employee form
- Delete employee
- Protected routes
- Logout

### DevOps
- Dockerized application
- Deployed on cloud (Render.com)
- Automated tests (8 tests, all passing)
- Environment variables for security

## Project Structure
employee-management-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── auth.py
│   ├── users.py
│   ├── documents.py
│   └── email.py
├── tests/
│   └── test_main.py
├── Dockerfile
├── requirements.txt
└── README.md

## API Endpoints

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/` | GET | Public | Welcome message |
| `/register` | POST | Public | Create account |
| `/login` | POST | Public | Get JWT token |
| `/me` | GET | Any user | View own profile |
| `/employees` | GET | Manager+ | List all employees |
| `/employees` | POST | Admin | Add employee |
| `/employees/{id}` | GET | Any user | Get one employee |
| `/employees/{id}` | PUT | Manager+ | Update employee |
| `/employees/{id}` | DELETE | Admin | Delete employee |
| `/documents/upload` | POST | Manager+ | Upload and summarize |
| `/documents` | GET | Manager+ | List documents |
| `/documents/{id}` | GET | Any user | Get document |

## Role System

| Role | Access Level | Permissions |
|------|-------------|-------------|
| Admin | 3 | Full access |
| Manager | 2 | View and Update |
| Employee | 1 | View own profile |

## Automated Tests

8 tests covering:
- Root endpoint
- User registration
- Login
- Wrong password rejection
- Protected route blocking
- Admin adding employee
- Employee role restriction
- Manager viewing employees

Run tests:
```bash
pytest tests/ -v
```

## How to Run Locally

**Step 1 — Clone the repo:**
```bash
git clone https://github.com/Krishnaveni1633/employee-management-api.git
cd employee-management-api
```

**Step 2 — Create virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Step 3 — Install dependencies:**
```bash
pip install -r requirements.txt
```

**Step 4 — Set up .env file:**
DATABASE_URL=postgresql://username:password@localhost:5432/employee_db
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

**Step 5 — Run the app:**
```bash
uvicorn app.main:app --reload
```

**Step 6 — Open docs:**
http://127.0.0.1:8000/docs

## Run with Docker

```bash
docker build -t employee-api .
docker run -d -p 8000:8000 employee-api
```

## Developer
**Krishnaveni** — Computer Engineering Student

GitHub: https://github.com/Krishnaveni1633
