#!/usr/bin/env python3
"""
Verification script to test if the entire system is working correctly.
Run this after both backend and frontend are running.
"""

import requests
import json
import sys
from datetime import datetime

# Color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

API_BASE_URL = 'http://localhost:8000/api'
FRONTEND_URL = 'http://localhost:3000'

class TestRunner:
    def __init__(self):
        self.results = {
            'passed': 0,
            'failed': 0,
            'tests': []
        }
        self.token = None
        self.user_id = None
    
    def print_header(self, text):
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}{text:^60}{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")
    
    def print_test(self, name, passed, message=""):
        status = f"{GREEN}✓ PASS{RESET}" if passed else f"{RED}✗ FAIL{RESET}"
        print(f"{status} - {name}")
        if message:
            print(f"  {message}")
        
        self.results['tests'].append({
            'name': name,
            'passed': passed,
            'message': message
        })
        
        if passed:
            self.results['passed'] += 1
        else:
            self.results['failed'] += 1
    
    def test_backend_running(self):
        """Test if backend is running"""
        try:
            response = requests.get(f'{API_BASE_URL}/', timeout=5)
            self.print_test("Backend Running", response.status_code < 500)
            return response.status_code < 500
        except requests.exceptions.ConnectionError:
            self.print_test("Backend Running", False, "Cannot connect to backend on port 8000")
            return False
        except Exception as e:
            self.print_test("Backend Running", False, str(e))
            return False
    
    def test_frontend_running(self):
        """Test if frontend is running"""
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            self.print_test("Frontend Running", response.status_code == 200)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            self.print_test("Frontend Running", False, "Cannot connect to frontend on port 3000")
            return False
        except Exception as e:
            self.print_test("Frontend Running", False, str(e))
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        try:
            username = f"testuser_{int(datetime.now().timestamp())}"
            payload = {
                'username': username,
                'email': f'{username}@test.com',
                'password': 'TestPassword123'
            }
            response = requests.post(
                f'{API_BASE_URL}/auth/register/',
                json=payload,
                timeout=5
            )
            
            success = response.status_code in [200, 201]
            message = response.json().get('message', '') if response.status_code < 400 else response.text[:100]
            
            self.print_test("User Registration", success, message)
            
            if success:
                self.username = username
                self.password = 'TestPassword123'
            
            return success
        except Exception as e:
            self.print_test("User Registration", False, str(e))
            return False
    
    def test_user_login(self):
        """Test user login"""
        try:
            payload = {
                'username': self.username,
                'password': self.password
            }
            response = requests.post(
                f'{API_BASE_URL}/auth/login/',
                json=payload,
                timeout=5
            )
            
            success = response.status_code in [200, 201]
            
            if success:
                data = response.json()
                self.token = data.get('token')
                message = f"Token: {self.token[:20]}..." if self.token else "No token received"
            else:
                message = response.text[:100]
            
            self.print_test("User Login", success, message)
            return success
        except Exception as e:
            self.print_test("User Login", False, str(e))
            return False
    
    def test_get_analytics(self):
        """Test getting analytics summary"""
        if not self.token:
            self.print_test("Get Analytics Summary", False, "No token available")
            return False
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f'{API_BASE_URL}/analytics/summary/',
                headers=headers,
                timeout=5
            )
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                message = f"Total Equipment: {data.get('total_equipment', 0)}"
            else:
                message = response.text[:100]
            
            self.print_test("Get Analytics Summary", success, message)
            return success
        except Exception as e:
            self.print_test("Get Analytics Summary", False, str(e))
            return False
    
    def test_get_datasets(self):
        """Test getting datasets list"""
        if not self.token:
            self.print_test("Get Datasets", False, "No token available")
            return False
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f'{API_BASE_URL}/datasets/',
                headers=headers,
                timeout=5
            )
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                count = len(data) if isinstance(data, list) else 0
                message = f"Datasets: {count}"
            else:
                message = response.text[:100]
            
            self.print_test("Get Datasets", success, message)
            return success
        except Exception as e:
            self.print_test("Get Datasets", False, str(e))
            return False
    
    def test_get_equipment(self):
        """Test getting equipment list"""
        if not self.token:
            self.print_test("Get Equipment", False, "No token available")
            return False
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f'{API_BASE_URL}/equipment/',
                headers=headers,
                timeout=5
            )
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                count = len(data) if isinstance(data, list) else 0
                message = f"Equipment: {count}"
            else:
                message = response.text[:100]
            
            self.print_test("Get Equipment", success, message)
            return success
        except Exception as e:
            self.print_test("Get Equipment", False, str(e))
            return False
    
    def test_unauthorized_access(self):
        """Test that endpoints require authentication"""
        try:
            response = requests.get(
                f'{API_BASE_URL}/datasets/',
                timeout=5
            )
            
            # Should fail without token
            success = response.status_code in [401, 403]
            message = "Correctly rejected unauthorized access" if success else "Endpoint is not protected"
            
            self.print_test("Unauthorized Access Protection", success, message)
            return success
        except Exception as e:
            self.print_test("Unauthorized Access Protection", False, str(e))
            return False
    
    def print_summary(self):
        """Print test summary"""
        total = self.results['passed'] + self.results['failed']
        passed = self.results['passed']
        failed = self.results['failed']
        
        self.print_header("TEST SUMMARY")
        
        print(f"Total Tests: {total}")
        print(f"{GREEN}Passed: {passed}{RESET}")
        print(f"{RED}Failed: {failed}{RESET}\n")
        
        if failed == 0:
            print(f"{GREEN}🎉 All tests passed! System is working correctly.{RESET}\n")
            return True
        else:
            print(f"{RED}⚠️  Some tests failed. Please check the issues above.{RESET}\n")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        self.print_header("SYSTEM VERIFICATION TEST")
        print(f"Testing at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Test infrastructure
        print(f"{YELLOW}Testing Infrastructure...{RESET}")
        backend_running = self.test_backend_running()
        frontend_running = self.test_frontend_running()
        
        if not backend_running:
            print(f"\n{RED}Backend is not running. Start it with: python manage.py runserver{RESET}")
            self.print_summary()
            return False
        
        # Test API endpoints
        print(f"\n{YELLOW}Testing API Endpoints...{RESET}")
        self.test_unauthorized_access()
        
        if self.test_user_registration():
            if self.test_user_login():
                self.test_get_analytics()
                self.test_get_datasets()
                self.test_get_equipment()
        
        # Print summary
        return self.print_summary()

if __name__ == '__main__':
    runner = TestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)
