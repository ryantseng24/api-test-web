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
        "credit_card": "4111-1111-1111-1111",
        "address": "123 Main St",
        "phone": "123-456-7890",
        "dob": "1990-01-01"
    }

# 模擬除錯資訊
@router.get("/debug")
def get_debug():
    # 回傳除錯資訊
    return {
        "debug": True,
        "version": "1.0.0",
        "environment": "production",
        "database": {
            "host": "localhost",
            "port": 5432,
            "user": "dbuser",
            "password": "dbpass"
        },
        "server": {
            "host": "0.0.0.0",
            "port": 8000,
            "workers": 4
        }
    }

# 模擬完整用戶資料
@router.get("/users")
def get_users():
    # 回傳完整用戶資料
    return {
        "users": [
            {
                "id": 1,
                "username": "user1",
                "email": "user1@example.com",
                "password": "hash1",
                "role": "user",
                "created_at": "2024-01-01",
                "last_login": "2024-03-15"
            },
            {
                "id": 2,
                "username": "user2",
                "email": "user2@example.com",
                "password": "hash2",
                "role": "admin",
                "created_at": "2024-01-02",
                "last_login": "2024-03-14"
            }
        ]
    } 