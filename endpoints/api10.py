from fastapi import APIRouter

router = APIRouter(prefix="/api10", tags=["API10: Insufficient Logging & Monitoring"])

# 模擬未記錄重要操作
@router.get("/no-log")
def no_log():
    # 這裡不記錄任何操作
    return {"msg": "這個API沒有任何存取日誌（不建議）"} 