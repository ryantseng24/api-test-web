from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from datetime import datetime

router = APIRouter(prefix="/api9", tags=["API9: Improper Assets Management"])

# 舊版 API 重定向到新版
@router.get("/old-api")
def old_api():
    return RedirectResponse(url="/api9/new-api", status_code=301)

# 新版 API
@router.get("/new-api")
def new_api():
    return {
        "msg": "這是新版 API",
        "version": "2.0.0",
        "last_updated": "2025-06-13"
    }

# v1 路徑重定向到新路徑
@router.get("/v1/users")
def v1_users():
    return RedirectResponse(url="/api9/users", status_code=301)

# 新路徑
@router.get("/users")
def users():
    return {
        "users": [
            {"id": 1, "name": "user1"},
            {"id": 2, "name": "user2"}
        ]
    }

# 已棄用的 API 重定向到新端點
@router.get("/deprecated")
def deprecated():
    return RedirectResponse(
        url="/api9/new-endpoint",
        status_code=301,
        headers={"X-Deprecated": "true", "X-New-Endpoint": "/api9/new-endpoint"}
    )

# 新端點
@router.get("/new-endpoint")
def new_endpoint():
    return {
        "msg": "這是新的端點",
        "replaced": "/api9/deprecated",
        "since": "2025-06-13"
    }

# 未使用的 API（保持不變）
@router.get("/unused")
def unused():
    return {
        "msg": "這個 API 已經不再使用",
        "last_used": "2025-01-01"
    } 