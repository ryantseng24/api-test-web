from fastapi import APIRouter, Form, HTTPException, Depends
from datetime import datetime, timedelta
import jwt

router = APIRouter(prefix="/api2", tags=["API2: Broken User Authentication"])

# 模擬用戶資料
USERS = {
    "admin": {"password": "123456", "role": "admin"},
    "user1": {"password": "password", "role": "user"}
}

# 模擬 JWT 密鑰
SECRET_KEY = "your-secret-key"

def create_token(username: str):
    # 模擬 JWT token 生成
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# 模擬簡單登入（無防爆破、弱密碼）
@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username not in USERS:
        raise HTTPException(status_code=400, detail="用戶不存在")
    
    if USERS[username]["password"] != password:
        raise HTTPException(status_code=400, detail="密碼錯誤")
    
    token = create_token(username)
    return {"msg": "登入成功", "token": token}

# 模擬個人資料（未驗證）
@router.get("/profile")
def get_profile():
    return {
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin",
        "note": "這是未驗證的個人資料存取"
    } 