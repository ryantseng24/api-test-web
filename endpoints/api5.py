from fastapi import APIRouter, Body

router = APIRouter(prefix="/api5", tags=["API5: Broken Function Level Authorization"])

# 模擬未授權的管理功能
@router.get("/admin")
def admin():
    return {"msg": "這是管理員功能，但未檢查權限即可存取"}

# 模擬未授權的用戶創建
@router.post("/users")
def create_user(user: dict = Body(...)):
    return {
        "msg": "成功創建用戶（未檢查權限）",
        "user": user
    }

# 模擬未授權的用戶刪除
@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {
        "msg": f"成功刪除用戶 {user_id}（未檢查權限）"
    } 