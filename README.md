# API Security Test Platform

這是一個基於 FastAPI 的 API 安全測試平台，針對 OWASP API Top 10 及 Log4j 弱點進行測試。

## 功能特點

- 完整實現 OWASP API Top 10 安全弱點測試案例
- 支援 Log4j (Log4Shell) 弱點測試
- 自動化流量生成器，模擬各種攻擊場景
- 基於 OpenAPI 3.0 規範的 API 文件
- 完整的日誌記錄系統

## 安裝步驟

1. 克隆專案
```bash
git clone https://github.com/your-username/api-test-web.git
cd api-test-web
```

2. 建立虛擬環境
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安裝依賴
```bash
pip install -r requirements.txt
```

4. 啟動服務
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 使用方式

1. API 文件
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

2. 測試流量生成器
```bash
python traffic_generator.py
```

## 專案結構

```
api-test-web/
├── app.py                 # 主應用程式
├── traffic_generator.py   # 測試流量生成器
├── requirements.txt       # 依賴套件
├── endpoints/            # API 端點
│   ├── api1.py          # Broken Object Level Authorization
│   ├── api2.py          # Broken User Authentication
│   ├── api3.py          # Excessive Data Exposure
│   ├── api4.py          # Lack of Resources & Rate Limiting
│   ├── api5.py          # Broken Function Level Authorization
│   ├── api6.py          # Mass Assignment
│   ├── api7.py          # Security Misconfiguration
│   ├── api8.py          # Injection
│   ├── api9.py          # Improper Assets Management
│   ├── api10.py         # Insufficient Logging & Monitoring
│   └── log4j.py         # Log4j (Log4Shell)
└── logs/                # 日誌檔案
```

## API 文件

完整的 API 文件可在 `/docs` 路徑下查看，包含：
- 所有端點的詳細說明
- 請求/回應範例
- 互動式測試介面

## 授權

MIT License
