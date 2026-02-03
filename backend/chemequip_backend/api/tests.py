"""
Tests for API endpoints
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from chemequip_backend.api.models import Dataset, Equipment
import io
from django.core.files.uploadedfile import SimpleUploadedFile


class UserAuthTestCase(TestCase):
    """Test cases for user authentication"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post('/api/users/register/', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
    
    def test_user_login(self):
        """Test user login"""
        # Create user first
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        response = self.client.post('/api/users/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/api/users/login/', {
            'username': 'nonexistent',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DatasetUploadTestCase(TestCase):
    """Test cases for CSV upload"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        from rest_framework.authtoken.models import Token
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_csv_upload(self):
        """Test CSV file upload"""
        csv_content = b"""Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-01,Pump,150.5,10.5,45.2
Heat Exchanger-01,Heat Exchanger,500.0,6.0,65.5"""
        
        file = SimpleUploadedFile(
            "test.csv",
            csv_content,
            content_type="text/csv"
        )
        
        response = self.client.post('/api/datasets/upload_csv/', {
            'file': file
        }, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('dataset', response.data)
        self.assertEqual(response.data['dataset']['equipment_count'], 2)
    
    def test_invalid_csv_format(self):
        """Test upload with invalid CSV format"""
        csv_content = b"""Invalid,Format
Data,Here"""
        
        file = SimpleUploadedFile(
            "test.csv",
            csv_content,
            content_type="text/csv"
        )
        
        response = self.client.post('/api/datasets/upload_csv/', {
            'file': file
        }, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_non_csv_file(self):
        """Test upload with non-CSV file"""
        file = SimpleUploadedFile(
            "test.txt",
            b"This is not a CSV",
            content_type="text/plain"
        )
        
        response = self.client.post('/api/datasets/upload_csv/', {
            'file': file
        }, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DatasetManagementTestCase(TestCase):
    """Test cases for dataset management"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        from rest_framework.authtoken.models import Token
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Create test dataset
        self.dataset = Dataset.objects.create(
            user=self.user,
            filename='test.csv',
            equipment_count=2
        )
    
    def test_list_datasets(self):
        """Test listing datasets"""
        response = self.client.get('/api/datasets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_dataset_detail(self):
        """Test getting dataset details"""
        response = self.client.get(f'/api/datasets/{self.dataset.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['filename'], 'test.csv')
