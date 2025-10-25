# Clerk Authentication Setup Guide

This guide will help you set up Clerk authentication for the Chimera project.

## Step 1: Create a Clerk Account

1. Go to [https://clerk.com](https://clerk.com)
2. Sign up for a free account
3. Click "Create Application"
4. Choose your application name (e.g., "Chimera")
5. Select your authentication options:
   - ✅ Email/Password
   - ✅ Email verification (recommended)
   - Optional: Social logins (Google, GitHub, etc.)

## Step 2: Get Your API Keys

After creating your application:

1. Go to the Clerk Dashboard
2. Navigate to **API Keys** in the left sidebar
3. Copy your keys:
   - **Publishable Key** (starts with `pk_test_...`)
   - **Secret Key** (starts with `sk_test_...`)

## Step 3: Configure Environment Variables

1. Copy the environment template:
   ```bash
   cp env.template .env
   ```

2. Edit `.env` and add your Clerk keys:
   ```env
   # PostgreSQL (keep your existing values)
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_DB=your_db_name
   DB_HOST=db
   DB_PORT=5432

   # Clerk Authentication
   CLERK_SECRET_KEY=sk_test_YOUR_SECRET_KEY_HERE
   CLERK_PUBLISHABLE_KEY=pk_test_YOUR_PUBLISHABLE_KEY_HERE
   ```

3. Create frontend `.env`:
   ```bash
   cd frontend
   cp .env.example .env
   ```

4. Edit `frontend/.env`:
   ```env
   REACT_APP_CLERK_PUBLISHABLE_KEY=pk_test_YOUR_PUBLISHABLE_KEY_HERE
   REACT_APP_API_URL=http://localhost:8000
   ```

## Step 4: Start the Application

1. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Wait for all services to start:**
   - Database: Port 5433
   - Backend API: Port 8000
   - Frontend: Port 3000

3. **Access the application:**
   - Open your browser to [http://localhost:3000](http://localhost:3000)

## Step 5: Test the Integration

1. **Sign Up:**
   - Click "Sign up" on the homepage
   - Enter your email and password
   - Verify your email (if enabled)

2. **Check the Dashboard:**
   - After signing in, you should see your dashboard
   - Your user info should be displayed
   - User is automatically created in the PostgreSQL database

3. **Test API Endpoints:**
   ```bash
   # Health check (public)
   curl http://localhost:8000/health

   # Get user info (requires authentication)
   # You'll need to get the token from the browser's network tab
   curl http://localhost:8000/api/users/me \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
   ```

## Clerk Dashboard Configuration

### Recommended Settings:

1. **Email Addresses:**
   - Enable email verification for security
   - Customize verification email templates

2. **User Profile:**
   - Decide which fields are required
   - Configure user metadata if needed

3. **Sessions:**
   - Default settings work well
   - Session duration: 7 days

4. **Security:**
   - Enable password strength requirements
   - Consider enabling 2FA for production

## Troubleshooting

### "Missing Clerk Publishable Key" Error
- Make sure you created the `frontend/.env` file
- Check that the key starts with `pk_test_`
- Restart the frontend service: `docker-compose restart frontend`

### "Invalid token" Error
- Check that `CLERK_SECRET_KEY` is set in the root `.env` file
- Ensure the backend service restarted after adding the key
- The token might have expired - try logging out and back in

### Frontend Can't Connect to Backend
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app.py`
- Look at browser console for errors

### Database Connection Issues
- Verify PostgreSQL is running: `docker-compose ps`
- Check database credentials in `.env`
- View logs: `docker-compose logs db`

## Architecture Overview

```
┌─────────────┐
│   Frontend  │  (React + Clerk)
│  Port 3000  │
└──────┬──────┘
       │ HTTP + JWT Token
       ▼
┌─────────────┐
│   Backend   │  (FastAPI)
│  Port 8000  │  - Verifies Clerk JWT
└──────┬──────┘  - Auto-creates users
       │
       ▼
┌─────────────┐
│  PostgreSQL │
│  Port 5433  │  - Stores user data
└─────────────┘  - Links via clerk_id
```

## Next Steps

1. **Customize the UI:**
   - Edit `frontend/src/App.js`
   - Modify colors in `frontend/tailwind.config.js`

2. **Add More Endpoints:**
   - Create diagnostic sessions
   - Manage buckets
   - Organize accounts

3. **Deploy to Production:**
   - Update Clerk to production keys
   - Use environment-specific `.env` files
   - Enable HTTPS for security

## Support

- Clerk Documentation: https://clerk.com/docs
- Clerk Support: support@clerk.com
- Project Issues: Create an issue in your repository

## Security Notes

⚠️ **Important:**
- Never commit `.env` files to git
- Use different keys for development and production
- Enable email verification in production
- Set up proper error handling
- Monitor Clerk dashboard for suspicious activity

