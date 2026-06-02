# Quick Django Integration & Execution Guide

This is a comprehensive blueprint on how to configure and run your Django REST Framework (DRF) backend alongside your React (Vite) frontend for your System Development Project.

---

## 1. Backend Setup (Django)

### A. Prerequisites
Make sure Python (3.9+) is installed. Create and activate a Virtual Environment inside your project root to keep dependencies contained:

```bash
# Create a virtual environment
python -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### B. Install Dependencies
Install Django, Django REST Framework, and the CORS headers package (critical for React frontends running on other ports):

```bash
pip install django djangorestframework django-cors-headers
```

### C. Configure settings.py
In your main Django project folder (e.g., `salon_project/settings.py`), modify these configurations:

```python
# settings.py

INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'django_backend', # Register your custom salon app
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # MUST be placed high up in the middleware stack
    'django.middleware.common.CommonMiddleware',
    ...
]

# CORS Authorization settings for React local development (typically on port 5173 or 3000)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
]

# (Optional) For Dev simplicity, allow credentials & session transfers
CORS_ALLOW_CREDENTIALS = True

# SQLite database registration (Default)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}
```

### D. Prepare Database & Admin Account
Generate the models schema tables inside the SQLite file, and create an admin user to access the Admin Panel:

```bash
# Generate translation migrations
python manage.py makemigrations

# Execute schema setup onto SQLite
python manage.py migrate

# Create the administrative admin account
python manage.py createsuperuser
```

### E. Fire Up current python backend
```bash
python manage.py runserver 8000
```
This runs the Django REST Framework API live at `http://127.0.0.1:8000/api/`.

---

## 2. Frontend Setup (React & Vite)

### A. Run dependencies install
```bash
npm install
```

### B. Connect React to your local Django server
The React code uses `fetch` to connect to `/api/services/` and `/api/appointments/`.
For React to work cleanly, we config the Vite proxy inside `vite.config.ts` to redirect `/api/` traffic automatically when running on localhost. This gets around manual CORS settings or absolute URL declarations:

```typescript
// vite.config.ts (Example configuration)
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
});
```

Now, any fetch request such as `fetch('/api/services/')` will automatically point toward the Django port `8000` instance, ensuring perfect integration!
