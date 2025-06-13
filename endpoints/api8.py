from fastapi import APIRouter, Query, Body

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
    # 直接將用戶輸入回傳（模擬）
    return {
        "input": input,
        "rendered": f"<div>{input}</div>"
    }

# 模擬命令注入
@router.post("/exec")
def exec_cmd(cmd: dict = Body(...)):
    # 直接執行用戶輸入的命令（模擬）
    command = cmd.get("cmd", "")
    return {
        "command": command,
        "result": f"模擬執行結果: {command}"
    } 