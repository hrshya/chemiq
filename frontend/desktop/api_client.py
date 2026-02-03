import os
import requests


class APIClient:
    """Simple API client for the Django backend.

    Configure `BASE_URL` to point to your running backend (default http://127.0.0.1:8000).
    """

    def __init__(self, base_url=None):
        self.base_url = base_url or os.environ.get('CHEMEQUIP_API_URL', 'http://127.0.0.1:8000')
        self.session = requests.Session()
        self.token = None

    def set_token(self, token):
        self.token = token
        self.session.headers.update({'Authorization': f'Token {token}'})

    def login(self, username, password):
        # Try common endpoints; update as needed for your backend
        url = f"{self.base_url}/api/auth/token/login/"
        resp = self.session.post(url, data={'username': username, 'password': password})
        if resp.ok:
            data = resp.json()
            token = data.get('auth_token') or data.get('token')
            if token:
                self.set_token(token)
            return resp

        # fallback to DRF token auth
        url2 = f"{self.base_url}/api-token-auth/"
        resp2 = self.session.post(url2, data={'username': username, 'password': password})
        if resp2.ok:
            data = resp2.json()
            token = data.get('token')
            if token:
                self.set_token(token)
        return resp2

    def upload_csv(self, file_path):
        url = f"{self.base_url}/api/datasets/upload/"
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/csv')}
            return self.session.post(url, files=files)

    def get_history(self):
        url = f"{self.base_url}/api/datasets/"
        return self.session.get(url)

    def get_summary(self, dataset_id):
        url = f"{self.base_url}/api/datasets/{dataset_id}/summary/"
        return self.session.get(url)
