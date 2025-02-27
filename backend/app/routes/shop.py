from fastapi import APIRouter
from app.crud import get_stock,check_low_stock, add_stock_item, update_stock,get_shop_sales
from app.models import StockItem

router = APIRouter(prefix="/shop", tags=["Retail Shop"])

@router.get("/sales")
async def fetch_shop_sales():
    sales = await get_shop_sales()
    return {"shop_sales": sales}

# Add new stock item
@router.post("/stock/add")
async def add_retail_stock(stock: StockItem):
    stock_id = await add_stock_item(stock, 'stock')
    return {"message": "Stock added", "stock_id": stock_id}

# Get stock details
@router.get("/stock")
async def fetch_retail_stock():
    stock = await get_stock()
    return {"stock": stock}

# Deduct stock after a sale
@router.put("/stock/update")
async def update_retail_stock(name: str, quantity_sold: float):
    return await update_stock('stock',name, quantity_sold)

# Check low stock and suggest orders
@router.get("/stock/low")
async def fetch_low_stock():
    low_stock = await check_low_stock('stock')
    return {"low_stock_items": low_stock}
