# API Documentation - Chemical Equipment Parameter Visualizer

## Base URL
```
http://localhost:8000/api/
```

## Authentication

The API uses **Token Authentication**. After login, you'll receive a token that must be included in all requests.

### Request Header:
```
Authorization: Token YOUR_TOKEN_HERE
```

---

## Endpoints

### 1. User Management

#### Register User
```
POST /api/users/register/
Content-Type: application/json

Request Body:
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password_123"
}

Response (201 Created):
{
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "",
        "last_name": ""
    },
    "token": "abc123xyz789..."
}
```

#### Login User
```
POST /api/users/login/
Content-Type: application/json

Request Body:
{
    "username": "john_doe",
    "password": "secure_password_123"
}

Response (200 OK):
{
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "",
        "last_name": ""
    },
    "token": "abc123xyz789..."
}
```

---

### 2. Dataset Management

#### List All Datasets
```
GET /api/datasets/
Headers: Authorization: Token YOUR_TOKEN

Response (200 OK):
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "filename": "equipment_data.csv",
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
    ]
}
```

#### Get Dataset Details
```
GET /api/datasets/{id}/
Headers: Authorization: Token YOUR_TOKEN

Response (200 OK):
{
    "id": 1,
    "filename": "equipment_data.csv",
    "uploaded_at": "2026-02-03T10:30:00Z",
    "summary_stats": { ... },
    "equipment_count": 14,
    "equipment": [
        {
            "id": 1,
            "name": "Pump-01",
            "equipment_type": "Pump",
            "flowrate": 150.5,
            "pressure": 10.5,
            "temperature": 45.2,
            "created_at": "2026-02-03T10:30:00Z"
        },
        ...
    ],
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "",
        "last_name": ""
    }
}
```

#### Upload CSV File
```
POST /api/datasets/upload_csv/
Content-Type: multipart/form-data
Headers: Authorization: Token YOUR_TOKEN

Request Body:
file: <CSV file>

Response (201 Created):
{
    "message": "CSV processed successfully",
    "dataset": {
        "id": 2,
        "filename": "new_equipment_data.csv",
        "uploaded_at": "2026-02-03T11:00:00Z",
        "summary_stats": { ... },
        "equipment_count": 10,
        "equipment": [ ... ],
        "user": { ... }
    }
}

Error Response (400 Bad Request):
{
    "error": "CSV must contain columns: Equipment Name, Type, Flowrate, Pressure, Temperature"
}
```

#### Get Dataset Equipment
```
GET /api/datasets/{id}/equipment/
Headers: Authorization: Token YOUR_TOKEN

Response (200 OK):
[
    {
        "id": 1,
        "name": "Pump-01",
        "equipment_type": "Pump",
        "flowrate": 150.5,
        "pressure": 10.5,
        "temperature": 45.2,
        "created_at": "2026-02-03T10:30:00Z"
    },
    {
        "id": 2,
        "name": "Heat Exchanger-01",
        "equipment_type": "Heat Exchanger",
        "flowrate": 500.0,
        "pressure": 6.0,
        "temperature": 65.5,
        "created_at": "2026-02-03T10:30:00Z"
    },
    ...
]
```

#### Generate PDF Report
```
GET /api/datasets/{id}/generate_pdf/
Headers: Authorization: Token YOUR_TOKEN

Response (200 OK):
[PDF File Download]
Header: Content-Disposition: attachment; filename="Report_equipment_data.pdf"
```

---

### 3. Analytics & Summary

#### Get User Summary
```
GET /api/summary/summary/
Headers: Authorization: Token YOUR_TOKEN

Response (200 OK):
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
            "filename": "equipment_data.csv",
            "uploaded_at": "2026-02-03T10:30:00Z",
            "equipment_count": 14,
            "summary_stats": { ... }
        }
    ]
}
```

---

### 4. Equipment Data

#### List All Equipment
```
GET /api/equipment/
Headers: Authorization: Token YOUR_TOKEN

Response (200 OK):
{
    "count": 14,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Pump-01",
            "equipment_type": "Pump",
            "flowrate": 150.5,
            "pressure": 10.5,
            "temperature": 45.2,
            "created_at": "2026-02-03T10:30:00Z"
        },
        ...
    ]
}
```

#### Get Equipment Details
```
GET /api/equipment/{id}/
Headers: Authorization: Token YOUR_TOKEN

Response (200 OK):
{
    "id": 1,
    "name": "Pump-01",
    "equipment_type": "Pump",
    "flowrate": 150.5,
    "pressure": 10.5,
    "temperature": 45.2,
    "created_at": "2026-02-03T10:30:00Z"
}
```

---

## CSV Format Requirements

The CSV file must contain exactly these columns:

| Column Name | Type | Description |
|-----------|------|-------------|
| Equipment Name | String | Name/ID of the equipment |
| Type | String | Equipment type (Pump, Compressor, Heat Exchanger, Reactor, Separator, Column, Other) |
| Flowrate | Float | Flow rate in L/min |
| Pressure | Float | Pressure in Bar |
| Temperature | Float | Temperature in °C |

### Example CSV:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-01,Pump,150.5,10.5,45.2
Pump-02,Pump,200.3,12.0,48.5
Heat Exchanger-01,Heat Exchanger,500.0,6.0,65.5
Reactor-01,Reactor,100.0,15.0,80.0
```

---

## Error Responses

### 400 Bad Request
```json
{
    "error": "Error message describing what went wrong"
}
```

### 401 Unauthorized
```json
{
    "error": "Invalid credentials"
}
```

### 404 Not Found
```json
{
    "error": "Dataset not found"
}
```

### 403 Forbidden
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid authentication |
| 403 | Forbidden - No permission to access resource |
| 404 | Not Found - Resource not found |
| 500 | Server Error - Internal server error |

---

## Usage Examples with cURL

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password_123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password_123"
  }'
```

### 3. Upload CSV
```bash
curl -X POST http://localhost:8000/api/datasets/upload_csv/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -F "file=@sample_equipment_data.csv"
```

### 4. Get Summary
```bash
curl -X GET http://localhost:8000/api/summary/summary/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 5. List Datasets
```bash
curl -X GET http://localhost:8000/api/datasets/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 6. Download PDF Report
```bash
curl -X GET http://localhost:8000/api/datasets/1/generate_pdf/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -o report.pdf
```

---

## Pagination

List endpoints support pagination with the following query parameters:

```
GET /api/datasets/?page=1&page_size=10
```

Response includes:
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/datasets/?page=2",
    "previous": null,
    "results": [ ... ]
}
```

---

## Data Types

### Equipment Types
- Pump
- Compressor
- Heat Exchanger
- Reactor
- Separator
- Column
- Other

### Numeric Fields
- **Flowrate**: Float (L/min)
- **Pressure**: Float (Bar)
- **Temperature**: Float (°C)

---

## Rate Limiting

Currently, there is no rate limiting configured. For production deployment, consider implementing rate limiting to prevent abuse.

---

## Versioning

Current API Version: **v1**
Base URL remains: `http://localhost:8000/api/`

---

## Support

For issues or questions about the API:
1. Check the [README.md](README.md) for setup and configuration
2. Review Django logs: `python manage.py runserver --verbosity 3`
3. Access Django admin for data inspection: `http://localhost:8000/admin/`
