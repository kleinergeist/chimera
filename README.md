# 🛡️ Chimera - Digital Identity Protection Platform

> **One you. Many faces. Zero regrets.**
>
> Chimera is a personal cyber security platform that helps you manage multiple online personas, monitor your digital footprint, and take control of your personal data privacy.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Authentication](#authentication)
- [Security Testing](#security-testing)
- [Development](#development)
- [Contributing](#contributing)

---

## 🎯 Overview

**Chimera** is a full-stack application built for a hackathon that demonstrates:

- **Persona Management**: Create and manage multiple online identities separately
- **Digital Footprint Monitoring**: Discover what personal information is publicly available
- **Account Organization**: Group discovered accounts into "buckets" for easy management
- **Privacy-First Design**: Built with security and user privacy in mind

The platform uses a **React + TypeScript** frontend with **FastAPI** backend, **PostgreSQL** database, and **Clerk** authentication.

### 🎓 Educational Note

This project includes **intentional security vulnerabilities** for hackathon demonstration and security testing purposes. See [Security Testing](#security-testing) section for details.

---

## ✨ Key Features

### 👤 Persona Management
- Create separate online identities for different purposes
- Organize personas into logical buckets (work, personal, gaming, etc.)
- Manage which accounts belong to which personas

### 🔍 Digital Footprint Discovery
- Search for accounts across platforms using usernames
- Discover compromised accounts in data breaches
- Track which personal information is publicly available

### 📊 Account Organization
- Group accounts by persona/bucket
- View all discovered accounts in one dashboard
- Track account metadata and platform information

### 🔐 Secure Authentication
- Clerk-based authentication integration
- JWT token verification
- Protected API endpoints with role-based access

### 📱 Responsive UI
- Modern React + TypeScript frontend
- Tailwind CSS styling with shadcn-ui components
- Real-time updates with Vite dev server

---

## 🛠️ Tech Stack

### Frontend
- **React** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn-ui** - High-quality UI components
- **Clerk** - Authentication provider
- **React Router** - Client-side routing

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **PyJWT** - JWT token handling
- **Uvicorn** - ASGI server

### Database
- **PostgreSQL** - Relational database
- **SQLAlchemy** - Database abstraction layer

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Python 3.x** - Backend runtime
- **Node.js** - Frontend runtime

---

## 📁 Project Structure

```
chimera/
├── frontend/                    # React + TypeScript frontend
│   ├── src/
│   │   ├── pages/              # Page components (Landing, Dashboard, etc.)
│   │   ├── components/         # Reusable UI components
│   │   ├── services/           # API client service
│   │   ├── App.js              # Main app component
│   │   └── index.js            # Entry point
│   ├── public/                 # Static assets
│   ├── package.json            # Dependencies
│   ├── tailwind.config.js      # Tailwind configuration
│   └── Dockerfile              # Frontend container config
│
├── backend/                     # FastAPI backend
│   ├── app.py                  # Main FastAPI application
│   ├── models.py               # SQLAlchemy ORM models
│   ├── auth.py                 # Authentication utilities
│   ├── seed_data.py            # Database seeding script
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # Backend container config
│   └── tests/                  # Test files
│       ├── test_models.py      # Model unit tests
│       └── db.py               # Database test utilities
│
├── docker-compose.yml          # Multi-container config
├── env.template                # Environment variables template
├── CLERK_SETUP.md              # Clerk authentication setup guide
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Docker** and **Docker Compose** (recommended)
- **Node.js 16+** and **npm** (for local frontend development)
- **Python 3.8+** (for local backend development)
- **Clerk Account** (free tier available at https://clerk.com)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chimera
   ```

2. **Copy environment template**
   ```bash
   cp env.template .env
   ```

3. **Configure environment variables** (edit `.env`):
   ```bash
   POSTGRES_USER=chimera_user
   POSTGRES_PASSWORD=chimera_password
   POSTGRES_DB=chimera_db
   
   # Get these from Clerk dashboard
   CLERK_SECRET_KEY=sk_test_your_secret_key
   CLERK_PUBLISHABLE_KEY=pk_test_your_publishable_key
   ```

4. **Start services with Docker Compose**
   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Local Development (Frontend)

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure Clerk environment**
   ```bash
   echo "REACT_APP_CLERK_PUBLISHABLE_KEY=pk_test_your_key" > .env.local
   echo "REACT_APP_API_URL=http://localhost:8000" >> .env.local
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

### Local Development (Backend)

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL connection**
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost:5432/chimera_db"
   ```

5. **Run development server**
   ```bash
   uvicorn app:app --reload --port 8000
   ```

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐
│    Frontend     │
│  React + TS     │
│  Port 3000      │
└────────┬────────┘
         │ HTTP + JWT
         ▼
┌─────────────────┐
│  Clerk Auth     │
│  (Cloud)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Backend      │
│   FastAPI       │
│  Port 8000      │
└────────┬────────┘
         │ SQL
         ▼
┌─────────────────┐
│   PostgreSQL    │
│   Database      │
│  Port 5432      │
└─────────────────┘
```

### Request Flow

1. **Frontend** sends HTTP request with JWT token (from Clerk)
2. **Clerk Auth** verifies the token (cloud-based authentication)
3. **Backend** validates token and verifies user via database
4. **Database** stores/retrieves user data
5. **Response** returns to frontend as JSON

### Authentication Flow

```
User Login
    ↓
Clerk SignIn Widget
    ↓
Clerk Issues JWT Token
    ↓
Frontend sends JWT with requests
    ↓
Backend validates JWT (get_clerk_user_id)
    ↓
Backend creates/retrieves User from DB
    ↓
Protected endpoint executes with user context
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication Header
All endpoints (except `/health`) require:
```
Authorization: Bearer <jwt_token>
```

### Health Check
```
GET /health
Response: {"status": "ok", "message": "Chimera API is running"}
```

### User Endpoints

#### Get Current User
```
GET /api/users/me
Response:
{
  "id": 1,
  "clerk_id": "user_123abc",
  "email": "user@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

### Session Endpoints

#### Get User Sessions
```
GET /api/sessions
Response:
{
  "count": 2,
  "sessions": [
    {
      "id": 1,
      "status": "completed",
      "created_at": "2024-01-15T10:30:00",
      "completed_at": "2024-01-15T11:30:00"
    }
  ]
}
```

### Bucket Endpoints

#### Get User Buckets
```
GET /api/buckets
Response:
{
  "count": 2,
  "buckets": [
    {
      "id": 1,
      "bucket_name": "Work Accounts",
      "description": "Professional online presence"
    }
  ]
}
```

#### Create Bucket
```
POST /api/buckets
Body: {
  "bucket_name": "Gaming",
  "description": "Gaming accounts and profiles"
}
Response: {"success": true}
```

#### Delete Bucket
```
DELETE /api/buckets/{bucket_id}
Response: {"success": true}
```

### Account Endpoints

#### Get All Discovered Accounts
```
GET /api/accounts
Response:
{
  "count": 5,
  "accounts": [
    {
      "id": 1,
      "account_name": "john_doe",
      "email": "john@example.com",
      "platform": "github",
      "metadata": {...},
      "bucket": {"id": 1, "name": "Work"},
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

#### Update Account Bucket Assignment
```
PUT /api/accounts/{account_id}/bucket
Body: {"bucket_id": 2}
Response: {"success": true}
```

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  clerk_id VARCHAR UNIQUE NOT NULL,
  email VARCHAR UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Buckets Table
```sql
CREATE TABLE user_buckets (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  bucket_name VARCHAR NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Accounts Table
```sql
CREATE TABLE discovered_accounts (
  id SERIAL PRIMARY KEY,
  session_id INTEGER REFERENCES diagnostic_sessions(id),
  account_name VARCHAR,
  email VARCHAR,
  platform VARCHAR,
  account_metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Account Assignments Table
```sql
CREATE TABLE account_assignments (
  id SERIAL PRIMARY KEY,
  account_id INTEGER REFERENCES discovered_accounts(id),
  bucket_id INTEGER REFERENCES user_buckets(id),
  assigned_at TIMESTAMP DEFAULT NOW()
);
```

### Sessions Table
```sql
CREATE TABLE diagnostic_sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  status VARCHAR (e.g., 'active', 'completed'),
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP
);
```

---

## 🔐 Authentication

### Clerk Setup

This project uses **Clerk** for authentication. Follow these steps:

1. **Create Clerk Account**
   - Visit https://clerk.com
   - Sign up for free account

2. **Create Application**
   - Go to Clerk Dashboard
   - Click "Create Application"
   - Choose authentication providers (Email + Social)

3. **Get API Keys**
   - Navigate to "API Keys"
   - Copy **Publishable Key** → `CLERK_PUBLISHABLE_KEY`
   - Copy **Secret Key** → `CLERK_SECRET_KEY`

4. **Configure Environment**
   - Add keys to `.env` file
   - Restart backend service

See [CLERK_SETUP.md](./CLERK_SETUP.md) for detailed setup guide.

### Token Validation

Backend validates tokens using:
```python
from auth import get_clerk_user_id, get_current_user

@app.get("/api/protected")
async def protected_endpoint(
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_info, db)
    # user is guaranteed to be authenticated
    return {"user": user}
```

---

## 🧪 Security Testing

### Intentional Vulnerabilities

This project includes **57+ intentionally vulnerable functions** for security testing and hackathon demonstration purposes. These are located in `backend/insecure_examples.py`.

### Available Security Tests

- **Aikido Security Scanner**: Detects OWASP Top 10 and CWE vulnerabilities
- **Vulnerability Documentation**: See `SECURITY_TEST_CASES_EXPANDED.md`
- **CWE Mapping**: All vulnerabilities mapped to CWE standards

### Running Security Tests

```bash
# Run Aikido security scan
aikido scan

# View scan results
aikido scan --format json > security_report.json

# Analyze specific vulnerability type
grep "CWE-89" backend/insecure_examples.py  # SQL Injection
grep "CWE-78" backend/insecure_examples.py  # Command Injection
```

### Vulnerability Categories

- ✅ Remote Code Execution (10)
- 🔴 Authentication & Authorization (11)
- 📊 Data Exposure & Validation (10)
- 📁 File Operations (6)
- 💉 Injection Attacks (8)
- 🔑 Cryptography Issues (8)
- 🌐 Network & SSRF (4)
- ⚙️ Configuration (4)

See `VULNERABILITIES_QUICK_REFERENCE.md` for complete list.

---

## 👨‍💻 Development

### Project Commands

#### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint
```

#### Backend
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app:app --reload --port 8000

# Run database migrations
alembic upgrade head

# Seed sample data
python seed_data.py

# Run tests
pytest

# Run security scan
aikido scan
```

#### Docker
```bash
# Build all services
docker-compose build

# Start services
docker-compose up

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Rebuild specific service
docker-compose up --build backend
```

### Code Style

- **Frontend**: ESLint + Prettier (TypeScript)
- **Backend**: Black + isort + Flake8 (Python)

### Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

---

## 📝 Environment Variables

Create `.env` file based on `env.template`:

```bash
# PostgreSQL Configuration
POSTGRES_USER=chimera_user
POSTGRES_PASSWORD=chimera_password
POSTGRES_DB=chimera_db
DB_HOST=db
DB_PORT=5432

# Clerk Authentication
CLERK_SECRET_KEY=sk_test_your_secret_key_here
CLERK_PUBLISHABLE_KEY=pk_test_your_publishable_key_here

# Frontend (when running locally)
REACT_APP_CLERK_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
REACT_APP_API_URL=http://localhost:8000
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Code Standards

- Write meaningful commit messages
- Add tests for new features
- Update documentation
- Follow existing code style

---

## 📄 License

This project is created for hackathon purposes. See LICENSE file for details.

---

## 📞 Support

- **Documentation**: See [CLERK_SETUP.md](./CLERK_SETUP.md) for authentication setup
- **Security Tests**: See [SECURITY_TEST_CASES_EXPANDED.md](./SECURITY_TEST_CASES_EXPANDED.md)
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Clerk Documentation](https://clerk.com/docs)
- [Docker Documentation](https://docs.docker.com/)

---

**Built with ❤️ for the hackathon** 🚀



<img width="2511" height="1254" alt="{86BF323D-4E0C-47C3-BABE-C6127DA962F5}" src="https://github.com/user-attachments/assets/aaffdb95-8374-420c-8854-abe82089371c" />

