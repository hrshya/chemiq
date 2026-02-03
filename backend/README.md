# Chemical Equipment Parameter Visualizer - Backend

Django REST API for chemical equipment data visualization and analytics.

## Project Structure

```
backend/
├── chemequip_backend/          # Main Django project
│   ├── __init__.py
│   ├── settings.py            # Django configuration
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py                # WSGI configuration
│   └── api/                   # Main API app
│       ├── __init__.py
│       ├── models.py          # Database models (Dataset, Equipment)
│       ├── views.py           # API viewsets
│       ├── serializers.py     # DRF serializers
│       ├── urls.py            # API URL routing
│       ├── admin.py           # Django admin configuration
│       ├── utils.py           # CSV processing utilities
│       ├── pdf_utils.py       # PDF report generation
│       ├── apps.py            # App configuration
│       └── migrations/        # Database migrations
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── sample_data/
    └── sample_equipment_data.csv  # Sample test data
```

## Setup Instructions

### 1. Create Virtual Environment

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
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Server will be available at `http://localhost:8000/`

## API Endpoints

### Authentication

- **Register User**: `POST /api/users/register/`
  ```json
  {
    "username": "user123",
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```

- **Login**: `POST /api/users/login/`
  ```json
  {
    "username": "user123",
    "password": "securepassword"
  }
  ```

### Dataset Management

- **List Datasets**: `GET /api/datasets/`
  - Headers: `Authorization: Token YOUR_TOKEN`

- **Get Dataset Details**: `GET /api/datasets/{id}/`

- **Upload CSV**: `POST /api/datasets/upload_csv/`
  - Content-Type: multipart/form-data
  - Field: `file` (CSV file)

- **Get Dataset Equipment**: `GET /api/datasets/{id}/equipment/`

- **Generate PDF Report**: `GET /api/datasets/{id}/generate_pdf/`

### Analytics & Summary

- **Get User Summary**: `GET /api/summary/summary/`
  - Returns total equipment count, averages, and type distribution

### Equipment Data

- **List Equipment**: `GET /api/equipment/`

## CSV File Format

Expected CSV columns:
- **Equipment Name**: Name of the equipment (string)
- **Type**: Equipment type (string) - e.g., Pump, Compressor, etc.
- **Flowrate**: Flow rate value (float) - in L/min
- **Pressure**: Pressure value (float) - in Bar
- **Temperature**: Temperature value (float) - in °C

### Example CSV:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-01,Pump,150.5,10.5,45.2
Heat Exchanger-01,Heat Exchanger,500.0,6.0,65.5
Reactor-01,Reactor,100.0,15.0,80.0
```

## Features

✅ **User Authentication** - Token-based authentication with user registration/login
✅ **CSV Upload** - Upload and parse CSV files with equipment data
✅ **Data Validation** - Validates CSV format and data types
✅ **Analytics** - Calculates summary statistics (averages, min/max values)
✅ **History Management** - Stores last 5 uploaded datasets
✅ **PDF Reports** - Generate comprehensive PDF reports with charts and statistics
✅ **Database** - SQLite database for persistent data storage
✅ **Admin Interface** - Django admin panel for data management
✅ **CORS Support** - Configured for frontend applications (Web & Desktop)

## API Response Examples

### Upload CSV Response:
```json
{
  "message": "CSV processed successfully",
  "dataset": {
    "id": 1,
    "filename": "sample_equipment_data.csv",
    "uploaded_at": "2026-02-03T10:30:00Z",
    "equipment_count": 14,
    "summary_stats": {
      "total_equipment": 14,
      "avg_flowrate": 261.96,
      "avg_pressure": 9.64,
      "avg_temperature": 64.29,
      "equipment_type_distribution": {
        "Pump": 2,
        "Compressor": 2,
        "Heat Exchanger": 2,
        "Reactor": 2,
        "Separator": 2,
        "Column": 2,
        "Other": 2
      },
      "min_flowrate": 100.0,
      "max_flowrate": 500.0,
      "min_pressure": 5.0,
      "max_pressure": 16.5,
      "min_temperature": 35.0,
      "max_temperature": 92.5
    }
  }
}
```

### Summary Response:
```json
{
  "total_equipment": 14,
  "avg_flowrate": 261.96,
  "avg_pressure": 9.64,
  "avg_temperature": 64.29,
  "equipment_type_distribution": {
    "Pump": 2,
    "Compressor": 2,
    "Heat Exchanger": 2,
    "Reactor": 2,
    "Separator": 2,
    "Column": 2,
    "Other": 2
  },
  "recent_datasets": [
    {
      "id": 1,
      "filename": "sample_equipment_data.csv",
      "uploaded_at": "2026-02-03T10:30:00Z",
      "equipment_count": 14,
      "summary_stats": { ... }
    }
  ]
}
```

## Admin Interface

Access Django admin at: `http://localhost:8000/admin/`

Manage:
- **Users**: View all registered users
- **Datasets**: View uploaded CSV files and their statistics
- **Equipment**: View and manage individual equipment records

## Configuration

### CORS Settings

To allow requests from other applications, configure in `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # React frontend
    "http://localhost:5000",    # PyQt5 desktop app
]
```

### File Upload Limits

Current limits set in `settings.py`:
- Max file size: 10MB
- Upload directory: `/backend/media/datasets/`

## Testing

### Using sample_data.csv

1. Register a user:
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -d "username=testuser&email=test@example.com&password=testpass123"
```

2. Login and get token:
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -d "username=testuser&password=testpass123"
```

3. Upload CSV:
```bash
curl -X POST http://localhost:8000/api/datasets/upload_csv/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "file=@sample_data/sample_equipment_data.csv"
```

## Dependencies

- **Django 4.2.8**: Web framework
- **Django REST Framework 3.14.0**: REST API framework
- **Pandas 2.1.3**: CSV processing and data analysis
- **ReportLab 4.0.7**: PDF generation
- **django-cors-headers 4.3.1**: CORS support
- **python-dotenv 1.0.0**: Environment variables

## Next Steps

After backend setup is complete:

1. **Frontend (Web)**: Create React.js + Chart.js application
2. **Frontend (Desktop)**: Create PyQt5 + Matplotlib application
3. **Deployment**: Configure for production deployment

## Support & Documentation

For API documentation and testing, use:
- **Swagger UI**: Can be added using `drf-spectacular`
- **Postman**: Import API endpoints for testing
- **Django Admin**: Built-in admin interface at `/admin/`

