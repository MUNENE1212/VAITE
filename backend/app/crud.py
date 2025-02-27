from app.database import db
from app.models import CyberSale, ShopSale, RentalPayment,GasSale,StockItem, House
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException


# Cyber Café: Add Sale
async def add_cyber_sale(sale: CyberSale):
    result = await db.cyber_sales.insert_one(sale.dict())
    return str(result.inserted_id)

# Retail Shop: Add Sale
async def add_shop_sale(sale: ShopSale):
    result = await db.shop_sales.insert_one(sale.dict())
    return str(result.inserted_id)

# Rental Property: Add Payment
async def add_rental_payment(payment: RentalPayment):
    result = await db.rental_payments.insert_one(payment.dict())
    return str(result.inserted_id)

# Gas: Add Sale
async def add_gas_sale(sale: GasSale):
    result = await db.gas_sales.insert_one(sale.dict())
    return str(result.inserted_id)

# Fetch all cyber café sales
async def get_cyber_sales():
    sales = await db.cyber_sales.find().to_list(None)
    return [{**sale, "_id": str(sale["_id"])} for sale in sales]

# Fetch all shop sales
async def get_shop_sales():
    sales = await db.shop_sales.find().to_list(100)
    return [{**sale, "_id": str(sale["_id"])} for sale in sales]

# Fetch all rental payments
async def get_rental_payments():
    payments = await db.rental_payments.find().to_list(None)
    return [{**payment, "_id": str(payment["_id"])} for payment in payments]

# Fetch all gas sales
async def get_gas_sales():
    sales = await db.gas_sales.find().to_list(None)
    return [{**sale, "_id": str(sale["_id"])} for sale in sales]
from fastapi import HTTPException

# Add Stock
async def add_stock_item(stock: StockItem, collection_name: str):
    """ Adds stock item to the specified collection ('stock' or 'gas_stock'). """
    collection = db[collection_name]  # Get the correct MongoDB collection

    if stock.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity added must be greater than zero")

    existing_stock = await collection.find_one({"name": stock.name})

    if existing_stock:
        # If the item exists, update the quantity
        new_quantity = existing_stock["quantity"] + stock.quantity
        await collection.update_one(
            {"_id": existing_stock["_id"]},
            {"$set": {"quantity": new_quantity}}
        )
        return {
            "message": "Stock updated successfully",
            "item_id": str(existing_stock["_id"]),
            "new_quantity": new_quantity
        }

    else:
        # Insert new stock item if not found
        result = await collection.insert_one(stock.dict())
        return {
            "message": "New stock item added successfully",
            "item_id": str(result.inserted_id),
            "quantity": stock.quantity
        }
# Get all stock items
async def get_stock():
    items = await db.stock.find().to_list(None)
    return [{**item, "_id": str(item["_id"])} for item in items]

async def get_gas_stock():
    items = await db.gas_stock.find().to_list(None)
    return [{**item, "_id": str(item["_id"])} for item in items]



async def update_stock(collection_name: str, name: str, quantity_sold: float):
    collection = db[collection_name]
    item = await collection.find_one({"name": name})
    if item and item["quantity"] >= quantity_sold:
        new_quantity = item["quantity"] - quantity_sold
        await collection.update_one(
            {"name": name}, {"$set": {"quantity": new_quantity, "last_updated": datetime.utcnow()}}
        )
        return {"message": f"{collection_name} stock updated"}
    return {"error": "Insufficient stock"}


# Check for low stock and suggest purchase order
async def check_low_stock(collection_name: str):
    collection = db[collection_name]  # Dynamically select collection (stock or gas_stock)

    low_stock_items = await collection.find({"$expr": {"$lt": ["$quantity", "$min_stock"]}}).to_list(None)
    
    return [
        {
            "name": item["name"],
            "current_stock": item["quantity"],
            "min_stock": item["min_stock"],
            "suggested_order": item["min_stock"] * 2,  # Suggest double the minimum stock
            "supplier": item.get("supplier")  # Use `.get()` to avoid KeyErrors if supplier is missing
        }
        for item in low_stock_items
    ]
