from fastapi import APIRouter
from app.crud import get_cyber_sales
from app.models import CyberSale
from app.crud import add_cyber_sale
router = APIRouter(prefix="/cyber", tags=["Cyber Café"])

@router.get("/sales")
async def fetch_cyber_sales():
    sales = await get_cyber_sales()
    return {"cyber_sales": sales}

@router.post("/record")
async def add_cyber_service(service_data: CyberSale):
    return await add_cyber_sale(service_data)
