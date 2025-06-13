from fastapi import APIRouter, Body
import time
import asyncio

router = APIRouter(prefix="/api4", tags=["API4: Lack of Resources & Rate Limiting"])

# 模擬無資源限制的慢回應
@router.get("/slow")
def slow():
    time.sleep(5)  # 故意延遲
    return {"msg": "這是一個無資源限制的慢回應 (sleep 5s)"}

# 模擬大量請求處理
@router.post("/batch")
async def batch(items: list = Body(...)):
    # 無限制處理大量請求
    return {
        "msg": f"處理了 {len(items)} 個項目",
        "items": items[:10]  # 只回傳前 10 個項目
    }

# 模擬長時間請求
@router.get("/long")
async def long_request():
    # 模擬長時間運算
    await asyncio.sleep(10)
    return {"msg": "這是一個長時間請求 (sleep 10s)"} 