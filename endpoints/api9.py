from fastapi import APIRouter

router = APIRouter(prefix="/api9", tags=["API9: Improper Assets Management"])

# 模擬舊API未下架
@router.get("/old-api")
def old_api():
    return {"msg": "這是舊版API，應該要下架但還能存取"} 