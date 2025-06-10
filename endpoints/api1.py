from fastapi import APIRouter, Path

router = APIRouter(prefix="/api1", tags=["API1: Broken Object Level Authorization"])

# 模擬 Broken Object Level Authorization
@router.get("/user/{user_id}")
def get_user(user_id: int = Path(..., description="用戶ID")):
    # 實際應用應檢查權限，這裡直接回傳資料
    return {"user_id": user_id, "data": f"這是 user {user_id} 的敏感資料 (未檢查權限)"} 