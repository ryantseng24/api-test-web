from fastapi import APIRouter

router = APIRouter(prefix="/api7", tags=["API7: Security Misconfiguration"])

# 模擬開啟 debug 訊息
@router.get("/debug")
def debug():
    return {"debug": True, "msg": "這是開啟 debug 訊息的回應（不應在正式環境出現）"} 