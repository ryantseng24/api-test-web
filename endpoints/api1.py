from fastapi import APIRouter, Path, HTTPException

router = APIRouter(prefix="/api1", tags=["API1: Broken Object Level Authorization"])

# 模擬用戶資料
USERS = {
    1: {"id": 1, "name": "user1", "email": "user1@example.com", "role": "user"},
    2: {"id": 2, "name": "user2", "email": "user2@example.com", "role": "user"},
    3: {"id": 3, "name": "admin", "email": "admin@example.com", "role": "admin"}
}

# 模擬 Broken Object Level Authorization
@router.get("/user/{user_id}")
def get_user(user_id: int = Path(..., description="用戶ID")):
    # 實際應用應檢查權限，這裡直接回傳資料
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "data": f"這是 user {user_id} 的敏感資料 (未檢查權限)"}

# 模擬管理員功能
@router.get("/admin/users")
def get_all_users():
    # 實際應用應檢查管理員權限，這裡直接回傳所有用戶資料
    return {"users": list(USERS.values())} 