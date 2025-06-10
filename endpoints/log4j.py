from fastapi import APIRouter, Query
from loguru import logger

router = APIRouter(prefix="/log4j", tags=["Log4j (Log4Shell)"])

# 模擬 Log4Shell 弱點（僅供測試，請勿用於正式環境）
@router.get("/test")
def log4j_test(input: str = Query("")):
    # 將用戶輸入寫入 log，模擬 JNDI lookup
    logger.info(f"Log4j 測試輸入: {input}")
    return {"msg": "已寫入 log，請觀察是否有外部連線觸發（僅供測試）"} 