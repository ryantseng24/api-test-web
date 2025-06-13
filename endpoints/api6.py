from fastapi import APIRouter, Body

router = APIRouter(prefix="/api6", tags=["API6: Mass Assignment"])

# 模擬 Mass Assignment
@router.post("/profile")
def update_profile(data: dict = Body(...)):
    # 直接將用戶傳入的所有欄位寫入資料庫（模擬）
    return {"msg": "已更新（實際應驗證欄位）", "data": data}

# 模擬未驗證的用戶權限修改
@router.put("/user/{user_id}")
def update_user(user_id: int, data: dict = Body(...)):
    # 直接將用戶傳入的所有欄位寫入資料庫（模擬）
    return {
        "msg": f"已更新用戶 {user_id}（未驗證欄位）",
        "data": data
    }

# 模擬未驗證的系統設定修改
@router.patch("/settings")
def update_settings(data: dict = Body(...)):
    # 直接將用戶傳入的所有欄位寫入設定（模擬）
    return {
        "msg": "已更新系統設定（未驗證欄位）",
        "data": data
    } 