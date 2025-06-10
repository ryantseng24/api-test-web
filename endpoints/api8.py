from fastapi import APIRouter, Query

router = APIRouter(prefix="/api8", tags=["API8: Injection (SQLi, XSS)"])

# 模擬 SQL Injection
@router.get("/sqli")
def sqli(q: str = Query("")):
    # 直接將參數拼接進查詢字串（模擬）
    sql = f"SELECT * FROM users WHERE name = '{q}'"
    return {"query": sql, "result": f"模擬查詢結果 for {q}"}

# 模擬 XSS
@router.get("/xss")
def xss(input: str = Query("")):
    # 直接回顯用戶輸入
    return {"msg": f"你輸入了：{input}"} 