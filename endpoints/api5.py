from fastapi import APIRouter

router = APIRouter(prefix="/api5", tags=["API5: Broken Function Level Authorization"])

# 模擬未授權的管理功能
@router.get("/admin")
def admin():
    return {"msg": "這是管理員功能，但未檢查權限即可存取"} 