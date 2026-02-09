# Deployment Guide for Sovereign Youth

## Quick Deployment (Railway)

### 1. Deploy to Railway
1. Go to https://railway.app
2. Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `SovereignYouthDigitalCoil`
5. Click "Deploy Now"

### 2. Set Environment Variables
In Railway project settings, add:

```
SUPERUSER_USERNAME=admin
SUPERUSER_EMAIL=admin@cyberenigma.dev
SUPERUSER_PASSWORD=YourSecurePassword123!
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-url.railway.app
```

### 3. Access Your Site
- **Website**: `https://your-app-name.railway.app`
- **Admin Panel**: `https://your-app-name.railway.app/admin/`

### 4. Login
- **Username**: `admin`
- **Password**: Whatever you set in SUPERUSER_PASSWORD

## Alternative: Manual Superuser Creation

If automatic creation doesn't work:

### Railway Console:
1. Go to Railway → Your Project → Console
2. Run: `python manage.py createsuperuser`
3. Enter username, email, password

### Heroku CLI:
```bash
heroku run python manage.py createsuperuser
```

## Important Notes

- **Never commit passwords** to Git
- **Use environment variables** for secrets
- **Change default password** after first login
- **Keep SUPERUSER_PASSWORD secure**

## Staff Users (Already Created)
- terence (password: S0v3r31gnY0uth2025!)
- flora (password: Y0uthL34d3rFl0ra!)
- phillip (password: Ph1ll1pS0v3r31gn!)
- jovan (password: J0v4nC0achY0uth!)

These will need to be recreated in production or migrated from local database.
