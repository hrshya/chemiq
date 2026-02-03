# 🧪 Chemical Equipment Parameter Visualizer

A complete full-stack application for uploading, analyzing, and visualizing chemical equipment parameters using CSV data.

## 🎯 Project Overview

This application provides:
- **CSV Upload**: Upload equipment data in CSV format
- **Data Management**: Organize datasets and equipment information
- **Visualization**: Interactive charts and analytics dashboards
- **Parameter Analysis**: Filter, sort, and analyze equipment parameters
- **PDF Reports**: Generate downloadable reports
- **Multi-platform**: Web app and desktop app support

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser                          │
│              (React.js on localhost:3000)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓ HTTP/HTTPS
         ┌───────────────────────────┐
         │    CORS Proxy / Vite      │
         └────────────┬──────────────┘
                      │
                      ↓
         ┌───────────────────────────┐
         │  Django REST API          │
         │  (localhost:8000/api)     │
         ├───────────────────────────┤
         │  - Authentication         │
         │  - CSV Upload & Parse     │
         │  - Data Management        │
         │  - Analytics              │
         │  - PDF Generation         │
         └────────────┬──────────────┘
                      │
                      ↓
         ┌───────────────────────────┐
         │   SQLite Database         │
         │   - Users                 │
         │   - Datasets              │
         │   - Equipment             │
         └───────────────────────────┘
```

## 📁 Project Structure

```
fosse/
│
├── 📄 README.md (this file)
├── 📄 GETTING_STARTED.md (Setup instructions)
├── 🐍 verify_system.py (Test script)
├── 🔄 start_all.bat (Windows quick start)
├── 🔄 start_all.sh (Unix quick start)
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── setup_db.py
│   ├── db.sqlite3
│   ├── equipment_manager/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── api/
│   │   ├── models.py (Dataset, Equipment)
│   │   ├── views.py (API endpoints)
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── migrations/
│   └── docs/
│       ├── API.md
│       ├── SETUP.md
│       └── README.md
│
├── frontend/
│   ├── web/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   └── Sidebar.jsx
│   │   │   ├── pages/
│   │   │   │   ├── Login.jsx
│   │   │   │   ├── Register.jsx
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── Datasets.jsx
│   │   │   │   ├── Upload.jsx
│   │   │   │   ├── Equipment.jsx
│   │   │   │   └── Analytics.jsx
│   │   │   ├── services/
│   │   │   │   └── api.js
│   │   │   ├── context/
│   │   │   │   └── AuthContext.jsx
│   │   │   ├── styles/
│   │   │   │   ├── global.css
│   │   │   │   ├── navbar.css
│   │   │   │   ├── sidebar.css
│   │   │   │   ├── auth.css
│   │   │   │   ├── dashboard.css
│   │   │   │   ├── datasets.css
│   │   │   │   ├── upload.css
│   │   │   │   ├── equipment.css
│   │   │   │   └── analytics.css
│   │   │   ├── App.jsx
│   │   │   └── main.jsx
│   │   ├── public/
│   │   │   └── index.html
│   │   ├── package.json
│   │   ├── vite.config.js
│   │   ├── .gitignore
│   │   ├── SETUP.md
│   │   └── README.md
│   │
│   └── desktop/ (Optional - PyQt5)
│       ├── main.py
│       ├── requirements.txt
│       └── README.md
│
└── docs/
    ├── ARCHITECTURE.md
    ├── DATABASE.md
    ├── DEPLOYMENT.md
    └── TROUBLESHOOTING.md
```

## 🚀 Quick Start

### Option 1: Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend (in new terminal):**
```bash
cd frontend/web
npm install
npm run dev
```

### Option 2: Automated Setup (Windows)
```bash
# Double-click or run in PowerShell:
.\start_all.bat
```

### Option 3: Automated Setup (macOS/Linux)
```bash
bash start_all.sh
```

### Verify System
```bash
python verify_system.py
```

## 📊 Features

### 🔐 Authentication
- User registration with validation
- Secure login with JWT tokens
- Protected API endpoints
- Automatic session management

### 📤 Data Upload
- Drag-and-drop CSV file upload
- Real-time file validation
- Batch equipment creation
- Error reporting and logging

### 📊 Dashboard
- Summary statistics cards
- Equipment distribution charts
- Recent datasets overview
- Quick access to key metrics

### 📁 Dataset Management
- List all uploaded datasets
- View dataset details
- Download PDF reports
- Equipment type breakdown

### ⚙️ Equipment Management
- Grid view of all equipment
- Filter by equipment type
- Sort by parameters
- View detailed specifications

### 📈 Advanced Analytics
- Key metrics display
- Distribution charts
- Parameter analysis
- Summary reports

## 🔗 API Endpoints

### Authentication
```
POST   /api/auth/register/          - Register new user
POST   /api/auth/login/             - Login user
POST   /api/auth/logout/            - Logout user
```

### Datasets
```
GET    /api/datasets/               - List datasets
GET    /api/datasets/{id}/          - Get dataset details
POST   /api/datasets/upload/        - Upload CSV
GET    /api/datasets/{id}/pdf/      - Download PDF
GET    /api/datasets/{id}/equipment/ - Get dataset equipment
```

### Equipment
```
GET    /api/equipment/              - List all equipment
GET    /api/equipment/{id}/         - Get equipment details
GET    /api/equipment/?type=...     - Filter by type
```

### Analytics
```
GET    /api/analytics/summary/      - Get summary statistics
```

## 📋 CSV Format

Required columns in uploaded CSV:
- `Equipment Type` - String (e.g., "Pump", "Compressor")
- `Flowrate (L/min)` - Float
- `Pressure (Bar)` - Float
- `Temperature (°C)` - Float

Example:
```csv
Equipment Type,Flowrate (L/min),Pressure (Bar),Temperature (°C)
Pump,50.5,3.2,25.0
Compressor,100.0,5.0,30.0
Turbine,75.2,4.1,28.5
```

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.2.8
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite
- **Data Processing**: Pandas 2.1.3
- **PDF Generation**: ReportLab 4.0.7

### Frontend (Web)
- **Framework**: React 18.2.0
- **Bundler**: Vite 5.0.0
- **Routing**: React Router 6.20.0
- **HTTP Client**: Axios 1.6.2
- **Charts**: Chart.js 4.4.0
- **UI Framework**: Bootstrap 5.3.2

### Frontend (Desktop - Optional)
- **Framework**: PyQt5
- **HTTP Client**: Requests

## 🧪 Testing

### Test API
```bash
# Run verification script
python verify_system.py
```

### Test with cURL
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'

# Get analytics (use token from login response)
curl -X GET http://localhost:8000/api/analytics/summary/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## 🔒 Security Features

✅ Token-based authentication
✅ Protected API endpoints
✅ CORS configuration
✅ Input validation
✅ File upload validation
✅ Error handling and logging

## 🚢 Deployment

### Deploy Backend
```bash
# Using Gunicorn
pip install gunicorn
gunicorn equipment_manager.wsgi:application --bind 0.0.0.0:8000

# Using Docker
docker build -t fosse-backend .
docker run -p 8000:8000 fosse-backend
```

### Deploy Frontend
```bash
# Build
npm run build

# Deploy dist/ to:
# - Vercel
# - Netlify
# - AWS S3
# - Any static hosting
```

## 📚 Documentation

- [Getting Started Guide](./GETTING_STARTED.md)
- [Backend Setup](./backend/docs/SETUP.md)
- [API Documentation](./backend/docs/API.md)
- [Frontend Setup](./frontend/web/SETUP.md)
- [Frontend README](./frontend/web/README.md)

## 🐛 Troubleshooting

### Backend Issues
- **Port 8000 in use**: See [GETTING_STARTED.md](./GETTING_STARTED.md)
- **Database errors**: Run `python manage.py migrate --run-syncdb`
- **CORS errors**: Verify CORS_ALLOWED_ORIGINS in settings.py

### Frontend Issues
- **Port 3000 in use**: Run `npm run dev -- --port 3001`
- **Module errors**: Run `rm -rf node_modules && npm install`
- **Cannot connect to API**: Check backend is running on port 8000

See [GETTING_STARTED.md](./GETTING_STARTED.md) for detailed troubleshooting.

## ✅ Requirements Checklist

- [ ] Python 3.8+
- [ ] Node.js 16+
- [ ] pip (Python package manager)
- [ ] npm (Node package manager)
- [ ] Git (for version control)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is provided as-is for educational purposes.

## 🎯 Future Enhancements

- [ ] Desktop application (PyQt5)
- [ ] Database export (Excel, JSON)
- [ ] Advanced filtering and search
- [ ] User role management
- [ ] Multi-tenant support
- [ ] Real-time notifications
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Mobile application

## 📞 Support

For issues or questions:
1. Check [GETTING_STARTED.md](./GETTING_STARTED.md)
2. Review browser console (F12)
3. Check backend logs
4. Run `verify_system.py`

## 🎉 Getting Help

```bash
# View help
python verify_system.py

# Check logs
tail -f backend/logs/debug.log      # Backend logs
npm run dev                          # Frontend logs (console)

# Reset database
python backend/setup_db.py
```

---

## 🚀 Ready to Start?

1. **[Read the Getting Started Guide](./GETTING_STARTED.md)**
2. **Run Quick Start**: `.\start_all.bat` (Windows) or `bash start_all.sh` (Unix)
3. **Access Frontend**: http://localhost:3000
4. **Register & Login**: Create a test account
5. **Upload CSV**: Try with sample data
6. **Explore Analytics**: View dashboards and reports

**Happy coding! 💻**

---
