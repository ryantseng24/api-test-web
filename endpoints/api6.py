from fastapi import APIRouter, Body

router = APIRouter(prefix="/api6", tags=["API6: Mass Assignment"])

# 模擬 Mass Assignment
@router.post("/profile")
def update_profile(data: dict = Body(...)):
    # 直接將用戶傳入的所有欄位寫入資料庫（模擬）
    return {"msg": "已更新（實際應驗證欄位）", "data": data} 