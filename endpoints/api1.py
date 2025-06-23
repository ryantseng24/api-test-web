from fastapi import APIRouter, Path, HTTPException, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import json
import logging
import re

router = APIRouter(prefix="/api1", tags=["API1: Broken Object Level Authorization"])

# === Pydantic Models ===
class UserResponse(BaseModel):
    """標準用戶響應模型"""
    id: str = Field(..., description="用戶 ID")
    name: str = Field(..., description="用戶姓名")
    email: str = Field(..., description="用戶電子郵件")
    role: Optional[str] = Field(None, description="用戶角色")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "name": "Test User",
                "email": "test@example.com",
                "role": "user"
            }
        }

class CreditCardResponse(BaseModel):
    """信用卡響應模型 - 故意不安全的實現"""
    card_number: str = Field(..., description="完整信用卡號碼 (不安全)")
    expiry: str = Field(..., description="有效期限")
    cvv: str = Field(..., description="CVV 安全碼 (不安全)")
    name: str = Field(..., description="持卡人姓名")
    
    class Config:
        json_schema_extra = {
            "example": {
                "card_number": "4111111111111111",
                "expiry": "12/25",
                "cvv": "123",
                "name": "John Doe"
            }
        }

class PaymentRequest(BaseModel):
    """付款請求模型"""
    card_number: str = Field(..., min_length=16, max_length=16, description="16位信用卡號碼")
    expiry: str = Field(..., description="有效期限 (MM/YY)")
    cvv: str = Field(..., min_length=3, max_length=4, description="CVV 安全碼")
    name: str = Field(..., description="持卡人姓名")
    amount: float = Field(..., gt=0, description="付款金額")

class PaymentResponse(BaseModel):
    """付款響應模型"""
    status: str = Field(..., description="付款狀態")
    message: str = Field(..., description="付款訊息")
    transaction_id: Optional[str] = Field(None, description="交易 ID")

class DebugResponse(BaseModel):
    """除錯資訊響應模型 - 故意洩露敏感資訊"""
    database_connection: str = Field(..., description="資料庫連線字串 (不安全)")
    api_keys: List[str] = Field(..., description="API 金鑰列表 (不安全)")
    internal_ips: List[str] = Field(..., description="內部 IP 位址 (不安全)")
    credit_cards: Dict = Field(..., description="所有信用卡資料 (嚴重違反 PCI-DSS)")

class UsersListResponse(BaseModel):
    """用戶列表響應模型"""
    users: List[Dict] = Field(..., description="用戶列表")

# === 模擬資料 ===
USERS = {
    1: {"id": 1, "name": "user1", "email": "user1@example.com", "role": "user"},
    2: {"id": 2, "name": "user2", "email": "user2@example.com", "role": "user"},
    3: {"id": 3, "name": "admin", "email": "admin@example.com", "role": "admin"}
}

# 模擬資料庫中的信用卡資料（違反 PCI-DSS：明文存儲）
credit_cards = {
    "user1": {
        "card_number": "4111111111111111",
        "expiry": "12/25",
        "cvv": "123",
        "name": "John Doe"
    },
    "user2": {
        "card_number": "5500000000000004",
        "expiry": "03/26",
        "cvv": "456",
        "name": "Jane Smith"
    }
}

# === API Endpoints ===
@router.get("/", 
           summary="API1 根目錄",
           description="返回 API1 的基本資訊")
async def root():
    return {"message": "API1 Root - Broken Object Level Authorization Tests"}

@router.get("/user/{user_id}", 
           response_model=UserResponse,
           summary="取得用戶資訊",
           description="根據用戶 ID 取得用戶詳細資訊。此端點存在物件層級授權漏洞。")
async def get_user(user_id: str = Path(..., description="用戶 ID")):
    # 模擬用戶資料 - 故意不檢查授權
    user_data = {
        "id": user_id,
        "name": "Test User",
        "email": "test@example.com",
        "role": "user"
    }
    return user_data

@router.get("/v1/user/{user_id}",
           summary="取得用戶資訊 (舊版本)",
           description="舊版本端點，會重定向到新版本")
async def get_user_v1(user_id: str = Path(..., description="用戶 ID")):
    return RedirectResponse(url=f"/api1/user/{user_id}", status_code=301)

@router.get("/legacy/user/{user_id}",
           summary="取得用戶資訊 (遺留版本)",
           description="遺留版本端點，會重定向到新版本")
async def get_user_legacy(user_id: str = Path(..., description="用戶 ID")):
    return RedirectResponse(url=f"/api1/user/{user_id}", status_code=301)

@router.post("/payment",
            response_model=PaymentResponse,
            summary="處理付款",
            description="處理信用卡付款。此端點違反 PCI-DSS 標準，會記錄敏感資訊。")
async def process_payment(payment: PaymentRequest):
    # 違反 PCI-DSS：明文記錄信用卡資訊
    logging.info(f"Processing payment with card {payment.card_number}")
    
    # 違反 PCI-DSS：不安全的錯誤處理（洩露敏感資訊）
    try:
        if not re.match(r'^\d{16}$', payment.card_number):
            raise ValueError(f"Invalid card number: {payment.card_number}")
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Payment processing failed: {str(e)}"
        )
    
    return {
        "status": "success", 
        "message": "Payment processed",
        "transaction_id": f"txn_{payment.card_number[-4:]}"
    }

@router.get("/credit-card/{user_id}",
           response_model=CreditCardResponse,
           summary="取得信用卡資訊",
           description="取得用戶的信用卡資訊。嚴重違反 PCI-DSS：返回完整信用卡資料。")
async def get_credit_card(user_id: str = Path(..., description="用戶 ID")):
    # 違反 PCI-DSS：直接返回完整信用卡資訊
    if user_id in credit_cards:
        return credit_cards[user_id]
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/v1/credit-card/{user_id}",
           summary="取得信用卡資訊 (舊版本)",
           description="舊版本端點，會重定向到新版本")
async def get_credit_card_v1(user_id: str = Path(..., description="用戶 ID")):
    return RedirectResponse(url=f"/api1/credit-card/{user_id}", status_code=301)

@router.get("/debug",
           response_model=DebugResponse,
           summary="除錯資訊",
           description="返回系統除錯資訊。嚴重安全漏洞：洩露所有敏感資訊。")
async def debug_info():
    # 違反 PCI-DSS：洩露敏感資訊
    return {
        "database_connection": "mysql://root:password@localhost:3306/payment_db",
        "api_keys": ["sk_test_123", "sk_live_456"],
        "internal_ips": ["10.0.0.1", "10.0.0.2"],
        "credit_cards": credit_cards  # 違反 PCI-DSS：洩露所有信用卡資訊
    }

@router.get("/admin/users",
           response_model=UsersListResponse,
           summary="取得所有用戶",
           description="管理員功能：取得所有用戶列表。存在授權漏洞：未檢查管理員權限。")
def get_all_users():
    # 實際應用應檢查管理員權限，這裡直接回傳所有用戶資料
    return {"users": list(USERS.values())} 