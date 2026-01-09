# Complaint Triage System

An AI-powered web application designed to manage and prioritize customer complaints efficiently.

The system provides two main interfaces:

## Users
- Users can submit complaints through a public interface.
- Each complaint is automatically analyzed using AI for categorization and priority.

## Admin
- Admins authenticate using email and password.
- After login, admins are redirected to a dashboard where they can:
  - View and manage all complaints
  - Update complaint status
  - Generate AI-based reply drafts
  - Edit, regenerate, and send replies via email

---

## Features

- Public complaint submission
- AI-based complaint categorization and priority detection
- Secure admin authentication using JWT
- Admin dashboard for complaint management
- AI-generated reply drafts
- Email-based responses using SendGrid

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite (local development)
- Passlib (bcrypt)
- Groq API (AI-powered analysis)
- Twilio SendGrid API (email delivery)

### Frontend
- Vue.js
- Axios
- Vite


---

## Configuration

Sensitive values are managed using environment variables.

```bash
GROQ_API_KEY=your_groq_api_key
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=verified_sender@example.com

JWT_SECRET_KEY=your_secret_key
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=strongpassword

## Running the Backend (Local)
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

## API documentation:

http://localhost:8000/docs


## Running the frontend (Local)
cd frontend-vue
npm install
npm run dev

## frontend will be available at

http://localhost:5173


## Notes

- Admin routes are protected using JWT authentication

- No credentials or API keys are committed to the repository

- Each user runs the project with their own local database

## System Flow Diagram

┌──────────────┐
│    User      │
│ (Public UI)  │
└──────┬───────┘
       │
       │ Submit Complaint
       ▼
┌──────────────────────┐
│   Frontend (Vue.js)  │
└──────┬───────────────┘
       │ HTTP Request (Axios)
       ▼
┌────────────────────────────┐
│   Backend (FastAPI API)    │
│                            │
│  ┌──────────────────────┐ │
│  │ Complaint Validation │ │
│  └──────────┬───────────┘ │
│             │             │
│             ▼             │
│  ┌──────────────────────┐ │
│  │ AI Analysis (Groq)   │ │
│  │ - Category           │ │
│  │ - Priority           │ │
│  └──────────┬───────────┘ │
│             │             │
│             ▼             │
│  ┌──────────────────────┐ │
│  │ Database (SQLite)    │ │
│  └──────────────────────┘ │
└──────────┬─────────────────┘
           │
           │ Admin Login (JWT)
           ▼
┌────────────────────────────┐
│     Admin Dashboard        │
│                            │
│ - View Complaints          │
│ - Update Status            │
│ - Generate AI Reply        │
│ - Edit / Regenerate Reply  │
│ - Send Email               │
└──────────┬─────────────────┘
           │
           │ Email Response
           ▼
┌────────────────────────────┐
│     SendGrid Email API     │
└──────────┬─────────────────┘
           │
           ▼
┌──────────────┐
│    User      │
│ (Email Reply)│
└──────────────┘

