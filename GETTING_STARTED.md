# Getting Started - Full Application Setup

## 🎯 Overview

This is a **Chemical Equipment Parameter Visualizer** with:
- **Backend**: Django REST API (Python)
- **Frontend Web**: React with Vite (JavaScript/React)
- **Desktop**: PyQt5 (Python) - Optional

## 📋 Prerequisites

### For Backend
- Python 3.8 or higher
- pip (Python package manager)

### For Web Frontend
- Node.js 16 or higher
- npm (comes with Node.js)

## 🚀 Quick Setup (Complete Stack)

### 1️⃣ Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

✅ Backend runs on: **http://localhost:8000**

### 2️⃣ Web Frontend Setup

```bash
# Navigate to web frontend directory
cd frontend/web

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Web Frontend runs on: **http://localhost:3000**

### 3️⃣ Test the Integration

1. Open **http://localhost:3000** in your browser
2. Click "Register" and create a new account
3. Login with your credentials
4. Upload a sample CSV file
5. View analytics and equipment data

## 📂 Project Structure

```
fosse/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── setup_db.py
│   ├── db.sqlite3
│   ├── equipment_manager/
│   │   └── settings.py
│   ├── api/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── migrations/
│   └── docs/
│       ├── API.md
│       ├── SETUP.md
│       └── README.md
│
└── frontend/
    ├── web/
    │   ├── src/
    │   │   ├── components/
    │   │   ├── pages/
    │   │   ├── services/
    │   │   ├── context/
    │   │   ├── styles/
    │   │   ├── App.jsx
    │   │   └── main.jsx
    │   ├── public/
    │   ├── package.json
    │   ├── vite.config.js
    │   └── README.md
    │
    └── desktop/ (PyQt5 - Optional)
        ├── main.py
        ├── requirements.txt
        └── README.md
```

## 🔑 API Endpoints

All API endpoints use **token authentication**:

```bash
Authorization: Token YOUR_TOKEN_HERE
```

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user (optional)

### Datasets
- `GET /api/datasets/` - List all datasets
- `GET /api/datasets/{id}/` - Get dataset details
- `POST /api/datasets/upload/` - Upload CSV file
- `GET /api/datasets/{id}/pdf/` - Download PDF report

### Equipment
- `GET /api/equipment/` - List all equipment
- `GET /api/equipment/{id}/` - Get equipment details
- `GET /api/datasets/{id}/equipment/` - Get equipment from dataset

### Analytics
- `GET /api/analytics/summary/` - Get summary statistics

## 🛠️ Environment Variables

### Backend (`.env` in backend/)
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Frontend (`.env` in frontend/web/)
```env
VITE_API_URL=http://localhost:8000/api
```

## 📊 Sample CSV Format

Required columns:
- `Equipment Type` - e.g., "Pump", "Compressor", "Turbine"
- `Flowrate (L/min)` - Numeric value
- `Pressure (Bar)` - Numeric value
- `Temperature (°C)` - Numeric value

Example:
```csv
Equipment Type,Flowrate (L/min),Pressure (Bar),Temperature (°C)
Pump,50.5,3.2,25
Compressor,100,5.0,30
Turbine,75.2,4.1,28
```

## 🧪 Testing the Application

### Test User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'
```

### Test User Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### Get Summary Statistics
```bash
curl -X GET http://localhost:8000/api/analytics/summary/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

**Database errors:**
```bash
python manage.py migrate --run-syncdb
python manage.py flush --no-input
python manage.py migrate
```

**CORS errors:**
Ensure `CORS_ALLOWED_ORIGINS` includes `http://localhost:3000` in backend settings.

### Frontend Issues

**Port 3000 already in use:**
```bash
npm run dev -- --port 3001
```

**Dependencies issues:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Cannot connect to backend:**
1. Verify backend is running on port 8000
2. Check CORS is enabled
3. Verify API URL in frontend: `src/services/api.js`
4. Check browser console for network errors

## 📚 Documentation

- [Backend API Documentation](backend/docs/API.md)
- [Backend Setup Guide](backend/docs/SETUP.md)
- [Frontend Setup Guide](frontend/web/SETUP.md)
- [Frontend README](frontend/web/README.md)

## 🚀 Deployment

### Backend (Production)
```bash
# Use Gunicorn
pip install gunicorn
gunicorn equipment_manager.wsgi:application --bind 0.0.0.0:8000

# Or use Docker
docker build -t fosse-backend .
docker run -p 8000:8000 fosse-backend
```

### Frontend (Production)
```bash
# Build
npm run build

# Deploy dist/ folder to:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
# - Any static hosting service
```

## 📦 Dependencies

### Backend
- Django 4.2.8
- Django REST Framework 3.14.0
- Pandas 2.1.3
- ReportLab 4.0.7
- Python-decouple 3.8
- CORS headers 4.3.1

### Frontend
- React 18.2.0
- React Router 6.20.0
- Axios 1.6.2
- Chart.js 4.4.0
- Vite 5.0.0
- Bootstrap 5.3.2

## 🔒 Security Notes

⚠️ **For Development Only:**
- `DEBUG=True` in Django
- Token stored in localStorage
- CORS open to localhost

🔐 **For Production:**
- Set `DEBUG=False`
- Use secure token storage (HTTP-only cookies)
- Enable HTTPS
- Set proper CORS headers
- Use environment variables for secrets
- Enable CSRF protection
- Add rate limiting

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review browser console (DevTools)
3. Check backend logs: `python manage.py runserver`
4. Verify network requests in Network tab
5. Refer to respective documentation files

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Can register and login
- [ ] Can upload CSV file
- [ ] Charts render correctly
- [ ] Can download PDF reports
- [ ] Can filter and sort equipment

## 🎉 Next Steps

1. Complete the setup above
2. Register a test user
3. Upload sample CSV data
4. Explore the dashboard and analytics
5. Optional: Setup desktop application (PyQt5)
6. Optional: Deploy to production

---

**Happy coding! 🚀**
