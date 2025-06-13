from fastapi import APIRouter

router = APIRouter(prefix="/api9", tags=["API9: Improper Assets Management"])

# 模擬舊版 API
@router.get("/old-api")
def old_api():
    return {
        "msg": "這是舊版 API，應該已經棄用",
        "version": "1.0.0",
        "deprecated": True
    }

# 模擬舊版路徑
@router.get("/v1/users")
def v1_users():
    return {
        "msg": "這是舊版路徑，應該使用 /api9/users",
        "version": "1.0.0",
        "deprecated": True
    }

# 模擬已棄用 API
@router.get("/deprecated")
def deprecated():
    return {
        "msg": "這個 API 已經棄用，請使用新版本",
        "new_endpoint": "/api9/new",
        "deprecated_since": "2024-01-01"
    }

# 模擬未使用 API
@router.get("/unused")
def unused():
    return {
        "msg": "這個 API 已經不再使用",
        "last_used": "2023-12-31",
        "replacement": None
    } 