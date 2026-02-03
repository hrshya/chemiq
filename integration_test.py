"""
Comprehensive Integration Test Suite
Tests the complete workflow from registration to analytics
"""

import requests
import json
import csv
import tempfile
import os
from datetime import datetime

# Configuration
API_URL = 'http://localhost:8000/api'
TIMEOUT = 10

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class IntegrationTester:
    def __init__(self):
        self.results = []
        self.token = None
        self.dataset_id = None
        self.test_timestamp = int(datetime.now().timestamp())
    
    def print_section(self, title):
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{title:^70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")
    
    def log_result(self, test_name, passed, details=""):
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"{status} {test_name}")
        if details:
            print(f"    {Colors.CYAN}→ {details}{Colors.RESET}")
        
        self.results.append({
            'test': test_name,
            'passed': passed,
            'details': details
        })
    
    def test_1_register_user(self):
        """Test user registration"""
        print("\n1️⃣  Testing User Registration...")
        
        try:
            username = f"testuser_{self.test_timestamp}"
            email = f"test_{self.test_timestamp}@example.com"
            password = "TestPass123!"
            
            payload = {
                'username': username,
                'email': email,
                'password': password
            }
            
            response = requests.post(
                f'{API_URL}/auth/register/',
                json=payload,
                timeout=TIMEOUT
            )
            
            if response.status_code in [200, 201]:
                self.username = username
                self.password = password
                data = response.json()
                message = f"User '{username}' created successfully"
                self.log_result("User Registration", True, message)
                return True
            else:
                self.log_result("User Registration", False, f"Status: {response.status_code} - {response.text[:100]}")
                return False
        
        except Exception as e:
            self.log_result("User Registration", False, str(e))
            return False
    
    def test_2_login_user(self):
        """Test user login and token retrieval"""
        print("\n2️⃣  Testing User Login...")
        
        try:
            payload = {
                'username': self.username,
                'password': self.password
            }
            
            response = requests.post(
                f'{API_URL}/auth/login/',
                json=payload,
                timeout=TIMEOUT
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.token = data.get('token')
                
                if self.token:
                    message = f"Token received: {self.token[:20]}..."
                    self.log_result("User Login", True, message)
                    return True
                else:
                    self.log_result("User Login", False, "No token in response")
                    return False
            else:
                self.log_result("User Login", False, f"Status: {response.status_code}")
                return False
        
        except Exception as e:
            self.log_result("User Login", False, str(e))
            return False
    
    def test_3_check_empty_datasets(self):
        """Check datasets before upload"""
        print("\n3️⃣  Checking Empty Datasets...")
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f'{API_URL}/datasets/',
                headers=headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else 0
                message = f"Found {count} datasets before upload"
                self.log_result("Check Datasets (Before Upload)", True, message)
                return True
            else:
                self.log_result("Check Datasets (Before Upload)", False, f"Status: {response.status_code}")
                return False
        
        except Exception as e:
            self.log_result("Check Datasets (Before Upload)", False, str(e))
            return False
    
    def test_4_upload_csv(self):
        """Test CSV file upload"""
        print("\n4️⃣  Testing CSV Upload...")
        
        try:
            # Create sample CSV
            csv_data = [
                ['Equipment Type', 'Flowrate (L/min)', 'Pressure (Bar)', 'Temperature (°C)'],
                ['Pump', '50.5', '3.2', '25.0'],
                ['Compressor', '100.0', '5.0', '30.0'],
                ['Turbine', '75.2', '4.1', '28.5'],
                ['Pump', '60.0', '3.5', '26.0'],
                ['Heat Exchanger', '80.0', '2.8', '40.0'],
            ]
            
            # Write to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                writer = csv.writer(f)
                writer.writerows(csv_data)
                temp_file = f.name
            
            # Upload file
            headers = {'Authorization': f'Token {self.token}'}
            
            with open(temp_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f'{API_URL}/datasets/upload/',
                    headers=headers,
                    files=files,
                    timeout=TIMEOUT
                )
            
            # Clean up
            os.unlink(temp_file)
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.dataset_id = data.get('id')
                message = f"CSV uploaded, Dataset ID: {self.dataset_id}, Equipment: {data.get('equipment_count', 0)}"
                self.log_result("CSV Upload", True, message)
                return True
            else:
                self.log_result("CSV Upload", False, f"Status: {response.status_code} - {response.text[:100]}")
                return False
        
        except Exception as e:
            self.log_result("CSV Upload", False, str(e))
            return False
    
    def test_5_get_datasets(self):
        """Test retrieving datasets"""
        print("\n5️⃣  Testing Get Datasets...")
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f'{API_URL}/datasets/',
                headers=headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else 0
                message = f"Retrieved {count} datasets"
                self.log_result("Get Datasets", True, message)
                return True
            else:
                self.log_result("Get Datasets", False, f"Status: {response.status_code}")
                return False
        
        except Exception as e:
            self.log_result("Get Datasets", False, str(e))
            return False
    
    def test_6_get_dataset_details(self):
        """Test retrieving specific dataset"""
        print("\n6️⃣  Testing Get Dataset Details...")
        
        if not self.dataset_id:
            self.log_result("Get Dataset Details", False, "No dataset ID available")
            return False
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f'{API_URL}/datasets/{self.dataset_id}/',
                headers=headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                message = f"Dataset: {data.get('filename', 'N/A')}, Equipment: {data.get('equipment_count', 0)}"
                self.log_result("Get Dataset Details", True, message)
                return True
            else:
                self.log_result("Get Dataset Details", False, f"Status: {response.status_code}")
                return False
        
        except Exception as e:
            self.log_result("Get Dataset Details", False, str(e))
            return False
    
    def test_7_get_equipment(self):
        """Test retrieving equipment"""
        print("\n7️⃣  Testing Get Equipment...")
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f'{API_URL}/equipment/',
                headers=headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else 0
                message = f"Retrieved {count} equipment items"
                self.log_result("Get Equipment", True, message)
                return True
            else:
                self.log_result("Get Equipment", False, f"Status: {response.status_code}")
                return False
        
        except Exception as e:
            self.log_result("Get Equipment", False, str(e))
            return False
    
    def test_8_get_analytics(self):
        """Test analytics summary"""
        print("\n8️⃣  Testing Analytics Summary...")
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f'{API_URL}/analytics/summary/',
                headers=headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                message = (
                    f"Total Equipment: {data.get('total_equipment', 0)}, "
                    f"Avg Flowrate: {data.get('avg_flowrate', 0):.2f} L/min, "
                    f"Avg Pressure: {data.get('avg_pressure', 0):.2f} Bar"
                )
                self.log_result("Analytics Summary", True, message)
                return True
            else:
                self.log_result("Analytics Summary", False, f"Status: {response.status_code}")
                return False
        
        except Exception as e:
            self.log_result("Analytics Summary", False, str(e))
            return False
    
    def test_9_filter_equipment(self):
        """Test equipment filtering"""
        print("\n9️⃣  Testing Equipment Filtering...")
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f'{API_URL}/equipment/?type=Pump',
                headers=headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else 0
                message = f"Found {count} Pump equipment items"
                self.log_result("Filter Equipment by Type", True, message)
                return True
            else:
                self.log_result("Filter Equipment by Type", False, f"Status: {response.status_code}")
                return False
        
        except Exception as e:
            self.log_result("Filter Equipment by Type", False, str(e))
            return False
    
    def test_10_pdf_generation(self):
        """Test PDF report generation"""
        print("\n🔟 Testing PDF Generation...")
        
        if not self.dataset_id:
            self.log_result("PDF Generation", False, "No dataset ID available")
            return False
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f'{API_URL}/datasets/{self.dataset_id}/pdf/',
                headers=headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                pdf_size = len(response.content)
                message = f"PDF generated, Size: {pdf_size} bytes"
                self.log_result("PDF Generation", True, message)
                return True
            else:
                self.log_result("PDF Generation", False, f"Status: {response.status_code}")
                return False
        
        except Exception as e:
            self.log_result("PDF Generation", False, str(e))
            return False
    
    def test_11_authentication_protection(self):
        """Test that endpoints require authentication"""
        print("\n1️⃣1️⃣  Testing Authentication Protection...")
        
        try:
            # Try to access without token
            response = requests.get(
                f'{API_URL}/datasets/',
                timeout=TIMEOUT
            )
            
            # Should be rejected
            is_protected = response.status_code in [401, 403]
            message = "Endpoints correctly require authentication" if is_protected else "Warning: Endpoint not protected"
            self.log_result("Authentication Protection", is_protected, message)
            return is_protected
        
        except Exception as e:
            self.log_result("Authentication Protection", False, str(e))
            return False
    
    def print_summary(self):
        """Print test summary"""
        passed = sum(1 for r in self.results if r['passed'])
        failed = sum(1 for r in self.results if not r['passed'])
        total = len(self.results)
        
        self.print_section("TEST SUMMARY")
        
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}✓ Passed: {passed}{Colors.RESET}")
        print(f"{Colors.RED}✗ Failed: {failed}{Colors.RESET}\n")
        
        if failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! System is working correctly.{Colors.RESET}\n")
        else:
            print(f"{Colors.RED}{Colors.BOLD}⚠️  SOME TESTS FAILED. Please review the failures above.{Colors.RESET}\n")
        
        # Detailed results
        print(f"{Colors.BOLD}Detailed Results:{Colors.RESET}")
        for i, result in enumerate(self.results, 1):
            status = f"{Colors.GREEN}✓{Colors.RESET}" if result['passed'] else f"{Colors.RED}✗{Colors.RESET}"
            print(f"{status} {i}. {result['test']}")
        
        print()
    
    def run_all_tests(self):
        """Run all integration tests"""
        self.print_section("COMPREHENSIVE INTEGRATION TESTS")
        print(f"Testing Full Workflow from Registration to Analytics")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        try:
            # Run tests in sequence
            if not self.test_1_register_user():
                print(f"\n{Colors.RED}Cannot proceed without registration{Colors.RESET}")
                return False
            
            if not self.test_2_login_user():
                print(f"\n{Colors.RED}Cannot proceed without login{Colors.RESET}")
                return False
            
            self.test_3_check_empty_datasets()
            
            if not self.test_4_upload_csv():
                print(f"\n{Colors.YELLOW}Skipping tests that require dataset{Colors.RESET}")
            else:
                self.test_5_get_datasets()
                self.test_6_get_dataset_details()
            
            self.test_7_get_equipment()
            self.test_8_get_analytics()
            self.test_9_filter_equipment()
            
            if self.dataset_id:
                self.test_10_pdf_generation()
            
            self.test_11_authentication_protection()
            
            # Print summary
            self.print_summary()
            
            return all(r['passed'] for r in self.results)
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
            return False
        except Exception as e:
            print(f"\n{Colors.RED}Unexpected error: {e}{Colors.RESET}")
            return False

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║     Chemical Equipment Parameter Visualizer - Integration Tests   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(Colors.RESET)
    
    print(f"\n{Colors.CYAN}Prerequisites:{Colors.RESET}")
    print("  ✓ Backend running on http://localhost:8000")
    print("  ✓ Database initialized")
    print(f"  {Colors.BOLD}Running tests...{Colors.RESET}\n")
    
    tester = IntegrationTester()
    success = tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
