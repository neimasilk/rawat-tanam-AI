#!/usr/bin/env python3
"""
Simple test script untuk testing endpoint tanpa pytest
"""

import requests
import time

def test_endpoint(url, description):
    """Test single endpoint"""
    try:
        print(f"\n🧪 Testing: {description}")
        print(f"📍 URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📄 Response: {data}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Run simple tests"""
    print("🌿 Starting Simple API Tests")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test endpoints
    tests = [
        (f"{base_url}/health", "Health Check"),
        (f"{base_url}/api/v1/info", "API Info"),
        (f"{base_url}/api/v1/species/stats", "Species Stats"),
        (f"{base_url}/api/v1/auth/tiers", "Auth Tiers"),
        (f"{base_url}/api/v1/species/", "Species List"),
    ]
    
    results = []
    for url, description in tests:
        success = test_endpoint(url, description)
        results.append((description, success))
        time.sleep(0.5)  # Small delay between tests
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    passed = 0
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {description}")
        if success:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check server logs.")

if __name__ == "__main__":
    main()