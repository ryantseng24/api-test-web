from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api7", tags=["API7: Security Misconfiguration"])

# 模擬開啟 debug 訊息
@router.get("/debug")
def debug():
    return {
        "debug": True,
        "msg": "這是開啟 debug 訊息的回應（不應在正式環境出現）",
        "stack_trace": "詳細的錯誤堆疊追蹤...",
        "environment": "production"
    }

# 模擬錯誤訊息
@router.get("/error")
def error():
    try:
        # 故意引發錯誤
        raise Exception("這是一個測試錯誤")
    except Exception as e:
        return {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": "詳細的錯誤追蹤...",
            "line": 10,
            "file": "api7.py"
        }

# 模擬設定資訊
@router.get("/config")
def config():
    return {
        "database": {
            "host": "localhost",
            "port": 5432,
            "user": "dbuser",
            "password": "dbpass"
        },
        "redis": {
            "host": "localhost",
            "port": 6379,
            "password": "redispass"
        },
        "jwt": {
            "secret": "your-secret-key",
            "algorithm": "HS256"
        }
    }

# 模擬版本資訊
@router.get("/version")
def version():
    return {
        "version": "1.0.0",
        "build": "20240315",
        "environment": "production",
        "dependencies": {
            "fastapi": "0.68.0",
            "uvicorn": "0.15.0",
            "python": "3.9.0"
        }
    } 