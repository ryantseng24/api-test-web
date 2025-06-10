from fastapi import APIRouter, Form

router = APIRouter(prefix="/api2", tags=["API2: Broken User Authentication"])

# 模擬簡單登入（無防爆破、弱密碼）
@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    # 密碼寫死，無防爆破
    if username == "admin" and password == "123456":
        return {"msg": "登入成功", "token": "fake-jwt-token"}
    return {"msg": "登入失敗"}

# 模擬未驗證存取個人資料
@router.get("/profile")
def profile():
    return {"user": "admin", "email": "admin@example.com", "note": "未驗證即可存取"} 