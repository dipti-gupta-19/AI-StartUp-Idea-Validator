# 🚀 AI Startup Idea Validator

An AI-powered startup idea evaluation platform built with **FastAPI**, **Streamlit**, **JWT Authentication**, **SQLite**, and **Google Gemini**. The application enables users to securely submit startup ideas and receive structured AI-generated evaluations across multiple business dimensions.

Designed as a scalable backend architecture, the project demonstrates authentication, REST API development, database integration, AI model orchestration, and modular software design.

---

## 📸 Demo


| Login | 
| <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/eff0988c-0d6a-4236-9737-65c4061a2ae8" />| 
| AI Evaluation |
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/07182f3f-2151-426d-80b7-4435d684c0d2" /> <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8a40d030-baf5-4d9b-9eb6-e719f5ad07de" /> <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/2e53fd00-5025-41f5-ba22-e167dc4f44e5" />

 | History |
 | <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/eaddd8f0-2940-41c5-83b2-2eac8b92bf78" />
 |

---

# Features

### 🔐 Secure Authentication
- JWT-based authentication
- User registration and login
- Protected API routes
- Token-based authorization

### 🤖 AI Startup Evaluation
Each submitted startup idea is evaluated using **Google Gemini** on:

- Creativity
- Market Demand
- Uniqueness
- Scalability
- Investment Readiness

Each category returns:

- AI-generated explanation
- Numerical score (1–10)

---

### 📊 Startup History

Every authenticated user can:

- Submit multiple startup ideas
- View previous evaluations
- Store results in a local SQL database

---

### 🗄 Database

- SQLAlchemy ORM
- SQLite
- Persistent storage of:
  - Users
  - Startup ideas
  - AI evaluations

---

### 📡 REST API

FastAPI provides fully documented REST APIs with Swagger UI.

Available endpoints include:

| Method | Endpoint | Description |
|---------|----------|------------|
| POST | `/signup` | Register new user |
| POST | `/login` | Authenticate user |
| POST | `/ideas` | Evaluate startup idea |
| GET | `/ideas/history` | Fetch previous evaluations |

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

# Tech Stack

| Category | Technology |
|----------|------------|
| Backend | FastAPI |
| Frontend | Streamlit |
| Authentication | JWT + OAuth2 |
| Database | SQLite |
| ORM | SQLAlchemy |
| AI Model | Google Gemini |
| Environment | python-dotenv |
| Validation | Pydantic |
| Language | Python |

---

# Project Structure

```text
AI-StartUp-Idea-Validator
│
├── src
│   ├── routers
│   │   ├── authentication.py
│   │   └── ideas.py
│   │
│   ├── database.py
│   ├── hashing.py
│   ├── model.py
│   ├── oauth2.py
│   ├── schema.py
│   ├── token.py
│   └── main.py
│
├── UI.py
├── requirements.txt
├── .env
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/dipti-gupta-19/AI-StartUp-Idea-Validator.git

cd AI-StartUp-Idea-Validator
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_API_KEY

SECRET_KEY=YOUR_SECRET_KEY

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

DATABASE_URL=sqlite:///./startup.db
```

---

# Running the Application

## Start FastAPI Backend

```bash
python -m uvicorn src.main:app --reload
```

Backend runs at

```
http://127.0.0.1:8000
```

Swagger API

```
http://127.0.0.1:8000/docs
```

---

## Start Streamlit Frontend

```bash
streamlit run UI.py
```

Frontend

```
http://localhost:8501
```

---

# AI Evaluation Response

Example:

```json
{
  "startup_idea": "AI Resume Reviewer",
  "evaluation": {
    "creativity": {
      "sentence": "...",
      "score": 8
    },
    "demand": {
      "sentence": "...",
      "score": 9
    },
    "uniqueness": {
      "sentence": "...",
      "score": 7
    },
    "scale": {
      "sentence": "...",
      "score": 8
    },
    "investment": {
      "sentence": "...",
      "score": 8
    }
  }
}
```

---

# Architecture

```
                Streamlit UI
                      │
                      ▼
               FastAPI Backend
                      │
        ┌─────────────┴──────────────┐
        │                            │
        ▼                            ▼
 JWT Authentication          Google Gemini API
        │                            │
        └─────────────┬──────────────┘
                      ▼
                SQLite Database
```

---

# Future Improvements

- AI report download (PDF)
- Email startup evaluation
- Team workspaces
- Idea comparison
- Startup score visualization
- Admin analytics dashboard
- Docker support
- CI/CD pipeline
- PostgreSQL support
- Deployment on Render / Railway / AWS

---

# Learning Outcomes

This project demonstrates practical experience with:

- REST API Development
- Authentication & Authorization
- JWT Security
- AI API Integration
- Prompt Engineering
- Database Design
- SQLAlchemy ORM
- FastAPI
- Streamlit
- Modular Backend Architecture
- Environment Variable Management
- API Documentation
- CRUD Operations

---

# License

This project is licensed under the MIT License.

---

## Author

**Dipti Gupta**

GitHub:
https://github.com/dipti-gupta-19
