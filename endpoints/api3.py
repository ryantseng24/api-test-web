from fastapi import APIRouter

router = APIRouter(prefix="/api3", tags=["API3: Excessive Data Exposure"])

# 模擬過度資料暴露
@router.get("/data")
def get_data():
    # 回傳過多敏感資料
    return {
        "user": "alice",
        "email": "alice@example.com",
        "password_hash": "123456hash",
        "ssn": "A123456789",
        "credit_card": "4111-1111-1111-1111"
    } 