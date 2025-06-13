from fastapi import APIRouter, Body
from datetime import datetime

router = APIRouter(prefix="/api10", tags=["API10: Insufficient Logging & Monitoring"])

# 模擬未記錄重要操作
@router.get("/no-log")
def no_log():
    # 這裡不記錄任何操作
    return {"msg": "這個API沒有任何存取日誌（不建議）"}

# 模擬登入操作
@router.post("/login")
def login(credentials: dict = Body(...)):
    # 模擬登入，但不記錄敏感資訊
    return {
        "msg": "登入成功",
        "timestamp": datetime.now().isoformat()
    }

# 模擬密碼修改
@router.put("/password")
def change_password(data: dict = Body(...)):
    # 模擬密碼修改，但不記錄操作
    return {
        "msg": "密碼已修改",
        "timestamp": datetime.now().isoformat()
    }

# 模擬用戶刪除
@router.delete("/user/{user_id}")
def delete_user(user_id: int):
    # 模擬用戶刪除，但不記錄操作
    return {
        "msg": f"用戶 {user_id} 已刪除",
        "timestamp": datetime.now().isoformat()
    } 