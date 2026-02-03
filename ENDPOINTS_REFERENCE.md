# API Endpoints Reference Card

## Quick Reference - All Endpoints

```
BASE_URL = http://localhost:8000/api/
```

---

## Authentication Endpoints

### Register User
```
POST /users/register/
Headers: Content-Type: application/json

Request:
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}

Response: 201 Created
{
  "user": {...},
  "token": "abc123xyz"
}
```

### Login User
```
POST /users/login/
Headers: Content-Type: application/json

Request:
{
  "username": "john_doe",
  "password": "secure_password"
}

Response: 200 OK
{
  "user": {...},
  "token": "abc123xyz"
}
```

---

## Dataset Endpoints

### List Datasets
```
GET /datasets/
Headers: Authorization: Token YOUR_TOKEN

Response: 200 OK
{
  "count": 2,
  "results": [...]
}
```

### Get Dataset Detail
```
GET /datasets/{id}/
Headers: Authorization: Token YOUR_TOKEN

Response: 200 OK
{
  "id": 1,
  "filename": "data.csv",
  "equipment_count": 14,
  "summary_stats": {...},
  "equipment": [...]
}
```

### Upload CSV File
```
POST /datasets/upload_csv/
Headers: Authorization: Token YOUR_TOKEN
Content-Type: multipart/form-data

Request:
file: <CSV_FILE>

Response: 201 Created
{
  "message": "CSV processed successfully",
  "dataset": {...}
}
```

### Get Equipment for Dataset
```
GET /datasets/{id}/equipment/
Headers: Authorization: Token YOUR_TOKEN

Response: 200 OK
[
  {
    "id": 1,
    "name": "Pump-01",
    "equipment_type": "Pump",
    "flowrate": 150.5,
    "pressure": 10.5,
    "temperature": 45.2
  },
  ...
]
```

### Generate PDF Report
```
GET /datasets/{id}/generate_pdf/
Headers: Authorization: Token YOUR_TOKEN

Response: 200 OK
[PDF File Download]
```

---

## Equipment Endpoints

### List All Equipment
```
GET /equipment/
Headers: Authorization: Token YOUR_TOKEN

Response: 200 OK
{
  "count": 14,
  "results": [...]
}
```

### Get Equipment Detail
```
GET /equipment/{id}/
Headers: Authorization: Token YOUR_TOKEN

Response: 200 OK
{
  "id": 1,
  "name": "Pump-01",
  "equipment_type": "Pump",
  "flowrate": 150.5,
  "pressure": 10.5,
  "temperature": 45.2
}
```

---

## Analytics Endpoints

### Get User Summary
```
GET /summary/summary/
Headers: Authorization: Token YOUR_TOKEN

Response: 200 OK
{
  "total_equipment": 14,
  "avg_flowrate": 261.96,
  "avg_pressure": 9.64,
  "avg_temperature": 64.29,
  "equipment_type_distribution": {
    "Pump": 2,
    "Compressor": 2,
    ...
  },
  "recent_datasets": [...]
}
```

---

## Endpoint Summary Table

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/users/register/` | Register new user | No |
| POST | `/users/login/` | Login & get token | No |
| GET | `/datasets/` | List user's datasets | Yes |
| GET | `/datasets/{id}/` | Get dataset details | Yes |
| POST | `/datasets/upload_csv/` | Upload CSV file | Yes |
| GET | `/datasets/{id}/equipment/` | Get equipment list | Yes |
| GET | `/datasets/{id}/generate_pdf/` | Download PDF report | Yes |
| GET | `/equipment/` | List all equipment | Yes |
| GET | `/equipment/{id}/` | Get equipment details | Yes |
| GET | `/summary/summary/` | Get user summary stats | Yes |

---

## cURL Command Examples

### 1. Register
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "pass123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "pass123"
  }'
```

### 3. Upload CSV
```bash
curl -X POST http://localhost:8000/api/datasets/upload_csv/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -F "file=@sample_data/sample_equipment_data.csv"
```

### 4. List Datasets
```bash
curl http://localhost:8000/api/datasets/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 5. Get Summary
```bash
curl http://localhost:8000/api/summary/summary/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 6. Download PDF
```bash
curl http://localhost:8000/api/datasets/1/generate_pdf/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -o report.pdf
```

---

## Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - No valid token |
| 403 | Forbidden - No permission |
| 404 | Not Found - Resource missing |
| 500 | Server Error |

---

## CSV Format

**Required Columns:**
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-01,Pump,150.5,10.5,45.2
Heat Exchanger-01,Heat Exchanger,500.0,6.0,65.5
```

**Equipment Types:**
- Pump
- Compressor
- Heat Exchanger
- Reactor
- Separator
- Column
- Other

---

## Access Levels

### Public (No Authentication Required)
- POST `/users/register/`
- POST `/users/login/`

### Authenticated (Token Required)
- All other endpoints

---

## Pagination

Add query parameters to list endpoints:
```
GET /datasets/?page=1&page_size=10
```

Response includes:
- `count`: Total records
- `next`: Next page URL
- `previous`: Previous page URL
- `results`: Array of records

---

## Error Handling

All errors return JSON:
```json
{
  "error": "Error message describing the problem"
}
```

Or detailed validation errors:
```json
{
  "field_name": ["Error message"]
}
```

---

## Token Header Format

Include token in every authenticated request:
```
Authorization: Token YOUR_TOKEN_HERE
```

Example:
```
Authorization: Token abc123xyz789def456ghi789jkl012
```

---

## Tips

1. **Save your token** after login - you'll need it for all requests
2. **Use pagination** for large datasets
3. **Check response status** before processing data
4. **Handle errors** gracefully in frontend
5. **Test with cURL first** before integrating into app

---

**Ready to integrate with your frontend app!**
