from fastapi import APIRouter
from app.crud import get_gas_sales,get_gas_stock,add_stock_item,update_stock
from app.models import StockItem
from app.crud import check_low_stock

router = APIRouter(prefix="/gas", tags=["Gas Business"])

@router.get("/sales")
async def fetch_gas_sales():
    sales = await get_gas_sales()
    return {"gas_sales": sales}

# Add gas stock
@router.post("/stock/add")
async def add_gas_stock_item(stock: StockItem):
    stock_id = await add_stock_item(stock, 'gas_stock')
    return {"message": "Gas stock added", "stock_id": stock_id}

# Get gas stock
@router.get("/stock")
async def fetch_gas_stock():
    stock = await get_gas_stock()
    return {"gas_stock": stock}

# Deduct stock after a sale
@router.put("/stock/update")
async def update_gas_stock(name: str, quantity_sold: float):
    return await update_stock('gas_stock',name, quantity_sold)

# Check low stock and suggest orders
@router.get("/stock/low")
async def fetch_low_gas_stock():
    low_stock = await check_low_stock('gas_stock')
    return {"low_stock_items": low_stock}