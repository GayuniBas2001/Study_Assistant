"""
Simple test script to verify backend functionality
Run with: python test_api.py
"""

import requests
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_status():
    """Test status endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/status", timeout=5)
        if response.status_code == 200:
            print("✓ Status check passed")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ Status check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Status check failed: {e}")
        return False

def test_root():
    """Test root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✓ Root endpoint passed")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ Root endpoint failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Root endpoint failed: {e}")
        return False

def main():
    print("Testing Study Assistant Backend API...")
    print("=" * 50)
    
    all_passed = True
    
    print("\n1. Testing root endpoint...")
    if not test_root():
        all_passed = False
    
    print("\n2. Testing health endpoint...")
    if not test_health():
        all_passed = False
    
    print("\n3. Testing status endpoint...")
    if not test_status():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Make sure the backend is running.")
        print("  Start backend with: python main.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
