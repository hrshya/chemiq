# Quick Start Guide - Backend Setup

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

## Installation Steps

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Run Setup Script

**On Windows:**
```bash
setup.bat
```

**On macOS/Linux:**
```bash
bash setup.sh
```

This will:
- Create a virtual environment
- Install all required dependencies
- Run database migrations
- Prepare the database

### Step 3: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. Example:
```
Username: admin
Email address: admin@example.com
Password: your_secure_password
Password (again): your_secure_password
```

### Step 4: Populate Sample Data (Optional)

To load the sample equipment data into the database:

```bash
python manage.py populate_sample_data
```

This creates a demo user with credentials:
- Username: `demouser`
- Password: `demo123456`

### Step 5: Run Development Server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000/`

## Accessing the Application

### Django Admin Interface
- **URL**: `http://localhost:8000/admin/`
- **Login**: Use the superuser credentials you created in Step 3

### API Endpoints
- **Base URL**: `http://localhost:8000/api/`
- **Documentation**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## First Time Setup Checklist

- [ ] Run setup script
- [ ] Create superuser
- [ ] (Optional) Populate sample data
- [ ] Start development server
- [ ] Test API endpoints
- [ ] Verify database in admin panel

## Testing the API

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

Response will contain your token.

### 2. Upload Sample CSV

```bash
curl -X POST http://localhost:8000/api/datasets/upload_csv/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -F "file=@sample_data/sample_equipment_data.csv"
```

### 3. Get Summary Statistics

```bash
curl -X GET http://localhost:8000/api/summary/summary/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Common Issues

### Issue: "Python not found"
- Ensure Python 3.8+ is installed
- Verify Python is in PATH: `python --version`

### Issue: Virtual environment not activating
- **Windows**: Use `venv\Scripts\activate.bat`
- **macOS/Linux**: Use `source venv/bin/activate`

### Issue: "No module named django"
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

### Issue: Database migration errors
- Delete `db.sqlite3` file if it exists
- Run: `python manage.py migrate`

### Issue: Port 8000 already in use
- Run on different port: `python manage.py runserver 8001`

## Project Structure

```
backend/
├── chemequip_backend/          # Main Django project
│   ├── settings.py             # Django configuration
│   ├── urls.py                 # URL routing
│   ├── wsgi.py                 # WSGI config
│   └── api/                    # API application
│       ├── models.py           # Database models
│       ├── views.py            # API views
│       ├── serializers.py      # Data serializers
│       ├── urls.py             # API URLs
│       └── ...
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── sample_data/                # Sample CSV files
├── README.md                   # Full documentation
├── API_DOCUMENTATION.md        # API reference
└── QUICKSTART.md              # This file
```

## Next Steps

1. **Setup Web Frontend**: Create React.js application
2. **Setup Desktop Frontend**: Create PyQt5 application
3. **Integration Testing**: Test all three components together
4. **Deployment**: Configure for production

## Database

The application uses **SQLite** by default, which is suitable for development. The database file is stored as `db.sqlite3` in the backend directory.

### Django Admin Features

Access `http://localhost:8000/admin/` to:
- Manage users
- View uploaded datasets
- Inspect equipment records
- View summary statistics

## Environment Variables

Create a `.env` file based on `.env.example` for custom configuration:

```bash
cp .env.example .env
```

Edit `.env` to customize settings like:
- Debug mode
- Allowed CORS origins
- Secret key
- File upload limits

## Stopping the Server

To stop the development server, press `Ctrl+C` in the terminal.

## Deactivating Virtual Environment

```bash
deactivate
```

## Reinstalling Dependencies

If you add new packages or encounter issues:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Help & Support

- Check [README.md](README.md) for detailed documentation
- Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
- Check Django logs for error messages
- Access Django admin for database inspection

---

**Ready to go!** Start the server and begin testing the API.
