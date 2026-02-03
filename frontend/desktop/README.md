# Chemical Equipment Parameter Visualizer — Desktop

This is a PyQt5 desktop frontend that talks to the Django REST backend used by the web app.

Quick start (Windows):

1. Create a virtual environment and install dependencies:

```powershell
cd frontend\desktop
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the app:

```powershell
venv\Scripts\python.exe main.py
```

3. Configure backend URL (optional):
- Set environment variable `CHEMEQUIP_API_URL` to the backend base URL (default `http://127.0.0.1:8000`).

Notes:
- The desktop app uses endpoints like `/api/datasets/` and `/api/datasets/upload/`. If your backend routes differ, update `api_client.py`.
- The app expects the backend to return JSON summaries with keys: `count`, `averages`, and `type_distribution`.
