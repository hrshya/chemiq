# 📖 Quick Reference Guide

## 🚀 Quick Start Commands

### Windows
```bash
# One-line start (admin terminal)
.\start_all.bat

# Or manual startup
cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver

# In new terminal:
cd frontend\web && npm install && npm run dev
```

### macOS/Linux
```bash
# One-line start
bash start_all.sh

# Or manual startup
cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver

# In new terminal:
cd frontend/web && npm install && npm run dev
```

---

## 🔗 Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | React web app |
| Backend API | http://localhost:8000 | Django REST API |
| Admin Panel | http://localhost:8000/admin | Django admin |
| API Root | http://localhost:8000/api | API endpoint base |

---

## 📝 Default Credentials

```
Admin User: (Create with: python manage.py createsuperuser)
Test User: Register in web app
```

---

## 🧪 Testing Commands

```bash
# Test system (checks if backend/frontend running)
python verify_system.py

# Integration tests (full workflow)
python integration_test.py

# Backend tests (if implemented)
cd backend && python manage.py test

# Frontend tests (if configured)
cd frontend/web && npm test
```

---

## 📁 File Locations

### Backend Key Files
```
backend/
├── manage.py                 # Django CLI
├── requirements.txt          # Python dependencies
├── db.sqlite3               # Database
├── equipment_manager/
│   └── settings.py          # Configuration
└── api/
    ├── models.py            # Database models
    ├── views.py             # API views
    └── urls.py              # Routes
```

### Frontend Key Files
```
frontend/web/
├── package.json             # Node dependencies
├── vite.config.js           # Vite config
├── src/
│   ├── App.jsx              # Main component
│   ├── services/
│   │   └── api.js           # API client
│   ├── pages/               # Page components
│   └── styles/              # CSS files
└── public/
    └── index.html           # HTML template
```

---

## 💾 Database Operations

### Reset Database
```bash
cd backend
python manage.py flush --no-input
python manage.py migrate
```

### Create Superuser
```bash
cd backend
python manage.py createsuperuser
```

### Run Migrations
```bash
cd backend
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

### Database Shell
```bash
cd backend
python manage.py shell
```

---

## 📦 NPM Commands (Frontend)

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Format code
npm run format
```

---

## 🐍 Python Commands (Backend)

```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Unix)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python manage.py runserver

# Run specific port
python manage.py runserver 0.0.0.0:8000

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests
python manage.py test

# Shell access
python manage.py shell
```

---

## 🔐 API Authentication

### Login to Get Token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"youruser","password":"yourpass"}'
```

### Use Token in Requests
```bash
curl -X GET http://localhost:8000/api/datasets/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## 📊 Sample CSV Format

```csv
Equipment Type,Flowrate (L/min),Pressure (Bar),Temperature (°C)
Pump,50.5,3.2,25.0
Compressor,100.0,5.0,30.0
Turbine,75.2,4.1,28.5
Heat Exchanger,80.0,2.8,40.0
```

---

## 🐛 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `netstat -ano \| findstr :8000` then kill process |
| Port 3000 in use | `npm run dev -- --port 3001` |
| Module not found | `pip install -r requirements.txt` or `npm install` |
| CORS error | Check `CORS_ALLOWED_ORIGINS` in Django settings |
| Database error | Run `python manage.py migrate` |
| Cannot login | Verify user exists, check credentials |
| Blank page | Clear cache (Ctrl+Shift+Del), clear localStorage |

---

## 🔍 Debugging Tips

### Check Backend Logs
```bash
# In terminal running backend
# Errors show directly in console
python manage.py runserver
```

### Check Frontend Logs
```bash
# Open browser Developer Tools (F12)
# View Console tab
npm run dev
```

### Test API Manually
```bash
# Use curl, Postman, or any HTTP client
curl -X GET http://localhost:8000/api/datasets/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Check Browser Console
```
F12 → Console tab
- Look for JavaScript errors
- Check network requests (Network tab)
- Check stored tokens (Application → Local Storage)
```

---

## 📖 Documentation Map

### Quick References
- This file: `QUICK_REFERENCE.md`
- Summary: `COMPLETION_SUMMARY.md`

### Main Documentation
- Project Overview: `README.md`
- Getting Started: `GETTING_STARTED.md`

### Backend Docs
- Backend Setup: `backend/docs/SETUP.md`
- API Reference: `backend/docs/API.md`
- Backend README: `backend/docs/README.md`

### Frontend Docs
- Frontend Setup: `frontend/web/SETUP.md`
- Frontend README: `frontend/web/README.md`

---

## 🎯 Project Structure at a Glance

```
fosse/
├── README.md                 ← START HERE
├── GETTING_STARTED.md        ← Setup guide
├── QUICK_REFERENCE.md        ← This file
├── COMPLETION_SUMMARY.md     ← What was built
│
├── verify_system.py          ← Test script
├── integration_test.py       ← Full tests
├── start_all.bat             ← Windows starter
├── start_all.sh              ← Unix starter
│
├── backend/                  ← Django API
│   ├── manage.py
│   ├── requirements.txt
│   ├── api/
│   └── docs/
│
└── frontend/
    └── web/                  ← React app
        ├── src/
        ├── package.json
        └── public/
```

---

## ⚡ Performance Tips

1. **Frontend**: Use `npm run build` for production
2. **Backend**: Use Gunicorn for production
3. **Database**: Use PostgreSQL for production
4. **Caching**: Implement Redis caching
5. **CDN**: Use for static files in production

---

## 🚀 Deployment Checklist

- [ ] Set `DEBUG=False` in Django
- [ ] Update `ALLOWED_HOSTS` in Django
- [ ] Configure `SECRET_KEY` (use environment variable)
- [ ] Setup production database (PostgreSQL recommended)
- [ ] Configure CORS for production domain
- [ ] Run `npm run build` for frontend
- [ ] Use HTTPS
- [ ] Setup backups
- [ ] Configure logging
- [ ] Setup monitoring/alerts

---

## 📞 Getting Help

1. **Check Documentation**: Start with README.md
2. **Run Tests**: `python verify_system.py`
3. **Check Logs**: 
   - Backend: Console output
   - Frontend: Browser F12 Console
4. **Check Database**: 
   - Backend Shell: `python manage.py shell`
   - SQL Query: View db.sqlite3

---

## 🎓 Learning Resources

### Django & REST Framework
- https://docs.djangoproject.com/
- https://www.django-rest-framework.org/

### React & Vite
- https://react.dev/
- https://vitejs.dev/

### Chart.js
- https://www.chartjs.org/

### Frontend Deployment
- Vercel: https://vercel.com
- Netlify: https://netlify.com

### Backend Deployment
- PythonAnywhere: https://www.pythonanywhere.com/
- Heroku: https://www.heroku.com/
- AWS: https://aws.amazon.com/

---

## 💡 Pro Tips

1. **Use Virtual Environment**: Always use venv for Python projects
2. **Install Dependencies**: Run `npm install` fresh after pulling code
3. **Clear Cache**: Use Ctrl+Shift+Del if seeing old content
4. **Check Console**: F12 in browser for JavaScript errors
5. **Use curl/Postman**: Test APIs before using in frontend
6. **Read Error Messages**: They usually tell you what's wrong
7. **Check Permissions**: Make sure ports aren't blocked
8. **Backup Database**: Regularly backup db.sqlite3
9. **Version Control**: Use git for tracking changes
10. **Document Changes**: Keep notes when modifying code

---

## 🔄 Regular Maintenance

```bash
# Weekly
npm audit
pip check

# Monthly
npm update
pip install --upgrade pip

# Before Deployment
npm run build
python manage.py test
python verify_system.py
python integration_test.py
```

---

## 📋 Useful Links

- Django Docs: https://docs.djangoproject.com/
- React Docs: https://react.dev/
- VS Code: https://code.visualstudio.com/
- Git Guide: https://git-scm.com/doc
- Python Docs: https://docs.python.org/3/

---

## 🎉 Quick Win

To verify everything works:
```bash
python verify_system.py
```

If all tests pass ✅, you're ready to go!

---

*Last Updated: 2024*
