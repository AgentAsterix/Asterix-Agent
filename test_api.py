#!/usr/bin/env python3
"""Quick test script to verify Aster Finance API connectivity."""

import requests
import time

def test_aster_api():
    """Test basic Aster Finance API connectivity."""
    print("🧪 Testing Aster Finance API Connectivity")
    print("=" * 45)
    
    # Test endpoints
    endpoints = [
        {
            "name": "Spot API - Server Time",
            "url": "https://sapi.asterdx.com/api/v1/time",
            "method": "GET"
        },
        {
            "name": "Spot API - Ping", 
            "url": "https://sapi.asterdx.com/api/v1/ping",
            "method": "GET"
        },
        {
            "name": "Futures API - Server Time",
            "url": "https://fapi.asterdx.com/fapi/v1/time", 
            "method": "GET"
        },
        {
            "name": "Futures API - Ping",
            "url": "https://fapi.asterdx.com/fapi/v1/ping",
            "method": "GET"
        }
    ]
    
    results = []
    
    for endpoint in endpoints:
        print(f"\n🌐 Testing {endpoint['name']}...")
        print(f"   URL: {endpoint['url']}")
        
        try:
            start_time = time.time()
            response = requests.get(
                endpoint['url'], 
                timeout=10,
                headers={'User-Agent': 'Agent-Aster/1.0.0'}
            )
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS - {response.status_code} ({response_time:.1f}ms)")
                try:
                    data = response.json()
                    if 'serverTime' in data:
                        server_time = data['serverTime']
                        print(f"   📅 Server Time: {server_time}")
                    else:
                        print(f"   📄 Response: {data}")
                except:
                    print(f"   📄 Response: {response.text[:100]}")
                results.append(True)
            else:
                print(f"   ❌ FAILED - HTTP {response.status_code}")
                print(f"   📄 Response: {response.text[:200]}")
                results.append(False)
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ TIMEOUT - No response after 10 seconds")
            results.append(False)
        except requests.exceptions.ConnectionError:
            print(f"   🌐 CONNECTION ERROR - Cannot reach server")
            results.append(False)
        except Exception as e:
            print(f"   ❌ ERROR - {e}")
            results.append(False)
    
    # Summary
    print(f"\n🎯 Test Results:")
    print("=" * 20)
    successful = sum(results)
    total = len(results)
    print(f"✅ Successful: {successful}/{total}")
    
    if successful == total:
        print("🟢 All Aster Finance APIs are reachable!")
        print("💡 You can now test with API keys")
    elif successful > 0:
        print("🟡 Some APIs are working")
        print("💡 Check network or try different endpoints")
    else:
        print("🔴 No APIs are reachable")
        print("💡 Check internet connection or VPN settings")
    
    return successful == total

def test_with_api_keys():
    """Test API with authentication (if keys are provided)."""
    api_key = "9889c4ca2a8612bbdc801df6f1fba74c6365b094df19d878b8a21a420e04436a"
    api_secret = "748c304002a5b1e4d841b079d636f0c8c8eeb96fb055f6b98684c65f56fe2fb3"
    
    print(f"\n🔐 Testing with API Keys...")
    print("=" * 30)
    
    # Test account endpoint with API key
    headers = {
        'X-MBX-APIKEY': api_key,  # Common format
        'x-api-key': api_key,     # Alternative format
        'User-Agent': 'Agent-Aster/1.0.0'
    }
    
    test_urls = [
        "https://sapi.asterdx.com/api/v1/account",
        "https://sapi.asterdx.com/api/v3/account", 
        "https://fapi.asterdx.com/fapi/v1/account",
        "https://fapi.asterdx.com/fapi/v2/account"
    ]
    
    for url in test_urls:
        print(f"\n🔑 Testing authenticated endpoint:")
        print(f"   URL: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS - API keys work!")
                data = response.json()
                print(f"   📄 Response keys: {list(data.keys())}")
                return True
            elif response.status_code == 401:
                print(f"   🔐 UNAUTHORIZED - Check API key format or permissions")
            elif response.status_code == 403:
                print(f"   🚫 FORBIDDEN - API key may be invalid or restricted")
            else:
                print(f"   ❓ HTTP {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
    
    return False

if __name__ == "__main__":
    # Test basic connectivity first
    basic_success = test_aster_api()
    
    if basic_success:
        # Test with API keys
        auth_success = test_with_api_keys()
        
        if auth_success:
            print(f"\n🎉 All tests passed! Ready to launch Agent-Aster")
        else:
            print(f"\n⚠️  Basic connectivity works, but API authentication needs checking")
    else:
        print(f"\n❌ Basic connectivity failed - check network connection")
    
    print(f"\n💡 Next steps:")
    print(f"   1. Fix any API issues above")
    print(f"   2. Launch web interface: python -m agent_aster.cli ui")
    print(f"   3. Test trading commands in safe mode")
