from fastapi import APIRouter, Request, Query, Header, HTTPException, Body
from fastapi.responses import JSONResponse, PlainTextResponse
from loguru import logger
import base64
import re
from typing import Optional, Dict, Any
from datetime import datetime

router = APIRouter(prefix="/cve", tags=["CVE: Real Vulnerability Simulations"])

# === CVE-2022-22965 (Spring4Shell) ===
@router.post("/spring4shell",
            summary="CVE-2022-22965 Spring4Shell RCE",
            description="模擬 Spring Framework RCE 漏洞。檢測 class.module.classLoader 參數模式。")
async def spring4shell(request: Request):
    """Spring4Shell 漏洞模擬 - 僅供安全測試使用"""
    body = await request.body()
    params = request.query_params
    
    # 檢測 Spring4Shell 特徵
    dangerous_patterns = [
        "class.module.classLoader",
        "class.module.classLoader.resources.context.parent.pipeline.first",
        "module.classLoader.resources",
        "class.classLoader.resources"
    ]
    
    for pattern in dangerous_patterns:
        if pattern in str(body) or pattern in str(params):
            logger.warning(f"Spring4Shell pattern detected: {pattern}")
            return {
                "vulnerable": True,
                "cve": "CVE-2022-22965",
                "pattern_detected": pattern,
                "message": "Spring4Shell vulnerability simulation triggered",
                "severity": "CRITICAL",
                "simulated_result": "RCE would be possible in vulnerable Spring application"
            }
    
    return {"vulnerable": False, "message": "No Spring4Shell patterns detected"}

# === CVE-2021-41773 (Apache Path Traversal) ===
@router.get("/apache/{path:path}",
           summary="CVE-2021-41773 Apache Path Traversal",
           description="模擬 Apache 2.4.49 路徑遍歷漏洞。")
async def apache_path_traversal(path: str):
    """Apache 路徑遍歷漏洞模擬"""
    # 檢測路徑遍歷模式
    traversal_patterns = [
        ".%2e/", "../", "..%2f", "%2e%2e/", "%2e%2e%2f",
        "..\\", "..%5c", "%2e%2e\\", "%2e%2e%5c",
        "....//", "....\\\\", "%252e%252e%252f"
    ]
    
    normalized_path = path.lower()
    
    for pattern in traversal_patterns:
        if pattern in normalized_path:
            logger.warning(f"Path traversal attempt detected: {path}")
            
            # 模擬敏感檔案內容
            if "etc/passwd" in normalized_path:
                return PlainTextResponse(
                    content="root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\n",
                    headers={"X-CVE": "CVE-2021-41773", "X-Vulnerable": "true"}
                )
            elif "windows/win.ini" in normalized_path:
                return PlainTextResponse(
                    content="; for 16-bit app support\n[fonts]\n[extensions]\n[mci extensions]\n",
                    headers={"X-CVE": "CVE-2021-41773", "X-Vulnerable": "true"}
                )
            else:
                return {
                    "vulnerable": True,
                    "cve": "CVE-2021-41773",
                    "path_requested": path,
                    "message": "Path traversal detected",
                    "simulated_access": f"Would access: /{path}"
                }
    
    return {"vulnerable": False, "path": path}

# === CVE-2014-6271 (Shellshock) ===
@router.get("/shellshock",
           summary="CVE-2014-6271 Shellshock",
           description="模擬 Bash Shellshock 漏洞。檢查 HTTP 標頭中的惡意模式。")
async def shellshock(
    request: Request,
    user_agent: Optional[str] = Header(None),
    referer: Optional[str] = Header(None),
    cookie: Optional[str] = Header(None)
):
    """Shellshock 漏洞模擬"""
    # Shellshock 特徵模式
    shellshock_pattern = r'\(\)\s*\{\s*[:|;]\s*\}\s*;'
    
    headers_to_check = {
        "User-Agent": user_agent,
        "Referer": referer,
        "Cookie": cookie,
        "X-Forwarded-For": request.headers.get("X-Forwarded-For"),
        "X-Real-IP": request.headers.get("X-Real-IP"),
        "Accept-Language": request.headers.get("Accept-Language")
    }
    
    for header_name, header_value in headers_to_check.items():
        if header_value and re.search(shellshock_pattern, header_value):
            logger.warning(f"Shellshock pattern detected in {header_name}: {header_value}")
            
            # 提取可能的命令
            command_match = re.search(r';\s*(.+)$', header_value)
            command = command_match.group(1) if command_match else "unknown command"
            
            return {
                "vulnerable": True,
                "cve": "CVE-2014-6271",
                "header": header_name,
                "pattern": header_value,
                "message": "Shellshock vulnerability simulation triggered",
                "simulated_command": command,
                "simulated_result": f"Command '{command}' would be executed"
            }
    
    return {"vulnerable": False, "message": "No Shellshock patterns detected"}

# === CVE-2017-5638 (Struts2 RCE) ===
@router.post("/struts2",
            summary="CVE-2017-5638 Apache Struts2 RCE",
            description="模擬 Struts2 Content-Type RCE 漏洞。")
async def struts2_rce(
    request: Request,
    content_type: Optional[str] = Header(None)
):
    """Struts2 RCE 漏洞模擬"""
    if content_type:
        # 檢測 OGNL 表達式
        ognl_patterns = [
            "%{", "${", "#_memberAccess", "@java.lang.Runtime",
            "processbuilder", "getruntime().exec", "#context",
            "@ognl.OgnlContext", "new java.lang.String"
        ]
        
        content_lower = content_type.lower()
        for pattern in ognl_patterns:
            if pattern.lower() in content_lower:
                logger.warning(f"Struts2 OGNL pattern detected: {pattern}")
                
                return {
                    "vulnerable": True,
                    "cve": "CVE-2017-5638",
                    "content_type": content_type,
                    "pattern_detected": pattern,
                    "message": "Struts2 RCE vulnerability simulation triggered",
                    "severity": "CRITICAL",
                    "simulated_result": "Remote code execution would be possible"
                }
    
    return {"vulnerable": False, "message": "No Struts2 OGNL patterns detected"}

# === CVE-2022-21449 (Psychic Signatures - JWT) ===
@router.post("/jwt-bypass",
            summary="CVE-2022-21449 Psychic Signatures",
            description="模擬 Java JWT ECDSA 簽名繞過漏洞。")
async def jwt_psychic_signatures(
    authorization: Optional[str] = Header(None)
):
    """JWT Psychic Signatures 漏洞模擬"""
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        
        try:
            # 解析 JWT (不驗證)
            parts = token.split(".")
            if len(parts) == 3:
                header = base64.b64decode(parts[0] + "==").decode('utf-8')
                
                # 檢查是否使用 ECDSA 算法且簽名為空
                if '"alg":"ES256"' in header or '"alg":"ES384"' in header or '"alg":"ES512"' in header:
                    signature = parts[2]
                    # 檢查簽名是否為特殊值（全零或特定模式）
                    if len(signature) == 0 or signature == "MAYCAQACAQA" or all(c == 'A' for c in signature):
                        logger.warning("JWT Psychic Signatures vulnerability detected")
                        return {
                            "vulnerable": True,
                            "cve": "CVE-2022-21449",
                            "algorithm": "ECDSA",
                            "message": "JWT signature bypass detected",
                            "severity": "HIGH",
                            "simulated_result": "Token would be accepted without valid signature"
                        }
        except:
            pass
    
    return {"vulnerable": False, "message": "No JWT bypass vulnerability detected"}

# === CVE-2021-44228 (Log4j) - 增強版 ===
@router.get("/log4j-enhanced/{path:path}",
           summary="CVE-2021-44228 Log4j RCE Enhanced",
           description="增強版 Log4j 漏洞檢測，支援多種繞過技術。")
@router.post("/log4j-enhanced/{path:path}")
async def log4j_enhanced(request: Request, path: str):
    """增強版 Log4j 漏洞模擬"""
    # 收集所有可能包含 payload 的地方
    potential_payloads = []
    
    # URL 路徑
    potential_payloads.append(path)
    
    # Query 參數
    for key, value in request.query_params.items():
        potential_payloads.extend([key, value])
    
    # Headers
    for key, value in request.headers.items():
        potential_payloads.extend([key, value])
    
    # Body (如果有)
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.body()
            potential_payloads.append(body.decode('utf-8'))
        except:
            pass
    
    # Log4j 模式（包含各種繞過）
    log4j_patterns = [
        r'\$\{jndi:',
        r'\$\{.*j.*n.*d.*i.*:',
        r'\$\{[^}]*:[^}]*\}',
        r'\$\{\s*j\s*n\s*d\s*i\s*:',
        r'\$\{.*\$\{.*\}.*\}',
        r'j\}n\}d\}i',
        r'\$\{env:.*:-j\}.*\$\{env:.*:-n\}',
        r'\$\{lower:j\}.*\$\{lower:n\}.*\$\{lower:d\}.*\$\{lower:i\}'
    ]
    
    for payload in potential_payloads:
        if payload:
            for pattern in log4j_patterns:
                if re.search(pattern, str(payload), re.IGNORECASE):
                    logger.warning(f"Advanced Log4j pattern detected: {payload[:100]}")
                    
                    # 提取 JNDI URL
                    jndi_match = re.search(r'(ldap|rmi|dns|ldaps|corba|iiop)://[^\}]+', str(payload))
                    jndi_url = jndi_match.group(0) if jndi_match else "obfuscated"
                    
                    return {
                        "vulnerable": True,
                        "cve": "CVE-2021-44228",
                        "pattern_location": "multiple",
                        "jndi_url": jndi_url,
                        "message": "Log4j RCE vulnerability detected",
                        "severity": "CRITICAL",
                        "obfuscation_detected": "$" not in payload[:10],
                        "simulated_result": f"JNDI lookup to {jndi_url} would be performed"
                    }
    
    return {"vulnerable": False, "message": "No Log4j patterns detected"}

# === CVE-2014-0160 (Heartbleed) ===
@router.post("/heartbleed",
            summary="CVE-2014-0160 Heartbleed",
            description="模擬 OpenSSL Heartbleed 資訊洩露漏洞。")
async def heartbleed(
    heartbeat_length: int = Body(default=16),
    heartbeat_data: str = Body(default="")
):
    """Heartbleed 漏洞模擬"""
    # 檢查是否請求過多數據
    if heartbeat_length > len(heartbeat_data) + 1000:
        logger.warning(f"Heartbleed attack detected: requested {heartbeat_length} bytes")
        
        # 模擬記憶體洩露
        leaked_data = {
            "vulnerable": True,
            "cve": "CVE-2014-0160",
            "requested_length": heartbeat_length,
            "actual_length": len(heartbeat_data),
            "message": "Heartbleed vulnerability simulation triggered",
            "severity": "HIGH",
            "leaked_memory": {
                "session_keys": "aes256:1234567890abcdef",
                "private_key_fragment": "-----BEGIN RSA PRIVATE KEY-----\nMIIE...",
                "user_data": "user=admin&password=secretpass123",
                "cookies": "session_id=abc123def456",
                "internal_data": "database_password=dbpass123"
            }
        }
        
        return leaked_data
    
    return {"vulnerable": False, "heartbeat_echo": heartbeat_data}

# === CVE-2019-5736 (runc Container Escape) ===
@router.post("/container-escape",
            summary="CVE-2019-5736 runc Container Escape",
            description="模擬容器逃逸漏洞。")
async def container_escape(command: Dict[str, Any] = Body(...)):
    """容器逃逸漏洞模擬"""
    cmd = command.get("cmd", "")
    
    # 檢測容器逃逸嘗試
    escape_patterns = [
        "/proc/self/exe", "/proc/1/", "nsenter",
        "mount.*proc", "chroot", "/host/", "docker.sock",
        "kubelet", "containerd", "runc"
    ]
    
    for pattern in escape_patterns:
        if re.search(pattern, cmd, re.IGNORECASE):
            logger.warning(f"Container escape attempt detected: {cmd}")
            
            return {
                "vulnerable": True,
                "cve": "CVE-2019-5736",
                "command": cmd,
                "pattern_detected": pattern,
                "message": "Container escape vulnerability simulation triggered",
                "severity": "HIGH",
                "simulated_result": "Container breakout to host would be possible"
            }
    
    return {"vulnerable": False, "command": cmd}

# === 漏洞摘要端點 ===
@router.get("/",
           summary="CVE 漏洞測試摘要",
           description="列出所有可用的 CVE 漏洞測試端點。")
async def cve_summary():
    """返回所有 CVE 測試端點摘要"""
    return {
        "message": "CVE Vulnerability Testing Endpoints",
        "warning": "僅供授權安全測試使用 - For authorized security testing only",
        "vulnerabilities": [
            {
                "cve": "CVE-2022-22965",
                "name": "Spring4Shell",
                "endpoint": "/cve/spring4shell",
                "severity": "CRITICAL",
                "description": "Spring Framework RCE via class.module.classLoader"
            },
            {
                "cve": "CVE-2021-41773",
                "name": "Apache Path Traversal",
                "endpoint": "/cve/apache/{path}",
                "severity": "HIGH",
                "description": "Apache 2.4.49 path traversal and RCE"
            },
            {
                "cve": "CVE-2014-6271",
                "name": "Shellshock",
                "endpoint": "/cve/shellshock",
                "severity": "CRITICAL",
                "description": "Bash environment variable code injection"
            },
            {
                "cve": "CVE-2017-5638",
                "name": "Struts2 RCE",
                "endpoint": "/cve/struts2",
                "severity": "CRITICAL",
                "description": "Apache Struts2 Content-Type OGNL injection"
            },
            {
                "cve": "CVE-2022-21449",
                "name": "Psychic Signatures",
                "endpoint": "/cve/jwt-bypass",
                "severity": "HIGH",
                "description": "Java ECDSA signature bypass"
            },
            {
                "cve": "CVE-2021-44228",
                "name": "Log4j (Enhanced)",
                "endpoint": "/cve/log4j-enhanced/{path}",
                "severity": "CRITICAL",
                "description": "Log4Shell JNDI injection with bypass techniques"
            },
            {
                "cve": "CVE-2014-0160",
                "name": "Heartbleed",
                "endpoint": "/cve/heartbleed",
                "severity": "HIGH",
                "description": "OpenSSL memory disclosure"
            },
            {
                "cve": "CVE-2019-5736",
                "name": "Container Escape",
                "endpoint": "/cve/container-escape",
                "severity": "HIGH",
                "description": "runc container breakout"
            }
        ]
    }