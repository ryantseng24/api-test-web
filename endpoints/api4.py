from fastapi import APIRouter
import time

router = APIRouter(prefix="/api4", tags=["API4: Lack of Resources & Rate Limiting"])

# 模擬無資源限制的慢回應
@router.get("/slow")
def slow():
    time.sleep(5)  # 故意延遲
    return {"msg": "這是一個無資源限制的慢回應 (sleep 5s)"} 