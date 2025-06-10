from fastapi import FastAPI, Request
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
from endpoints import api1, api2, api3, api4, api5, api6, api7, api8, api9, api10, log4j
import sys
import time
from pathlib import Path

# 設定日誌
log_path = Path("logs")
log_path.mkdir(exist_ok=True)

# 移除預設的處理器
logger.remove()

# 添加主控台輸出
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# 添加檔案輸出
logger.add(
    "logs/api_{time}.log",
    rotation="500 MB",  # 檔案大小達到 500MB 時輪替
    retention="10 days",  # 保留 10 天的日誌
    compression="zip",  # 壓縮舊日誌
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG"
)

app = FastAPI(title="API Security Test Platform",
              description="針對 OWASP API Top 10 及 Log4j 弱點的 API 測試站台",
              version="1.0.0")

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://apitest.ryantseng.work", "http://apitest.ryantseng.work"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 請求日誌中間件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {process_time:.2f}s"
    )
    
    return response

# 註冊各個弱點 endpoint
app.include_router(api1.router)
app.include_router(api2.router)
app.include_router(api3.router)
app.include_router(api4.router)
app.include_router(api5.router)
app.include_router(api6.router)
app.include_router(api7.router)
app.include_router(api8.router)
app.include_router(api9.router)
app.include_router(api10.router)
app.include_router(log4j.router)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"msg": "API Security Test Platform. See /docs for API list."} 