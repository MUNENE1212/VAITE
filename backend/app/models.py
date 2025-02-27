from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Cyber Café Model
class CyberSale(BaseModel):
    service: str
    price: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Retail Shop Sale Model
class ShopSale(BaseModel):
    item: str
    quantity: int
    price: float
    total_price: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Rental Payment Model
class RentalPayment(BaseModel):
    tenant_name: str
    house_number: str
    amount_paid: float
    month:str
    water_bill: float
    electricity_bill: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Gas Sale Model
class GasSale(BaseModel):
    item: str  # "Gas Refill" or "Gas Accessory"
    quantity: float  # Kg for gas, units for accessories
    price: float
    total_price: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Stock Model
class StockItem(BaseModel):
    name: str  # Item name (e.g., "Sugar 1kg", "Gas Refill 13kg")
    category: str  # "Retail" or "Gas"
    quantity: float  # Number of units or KG for gas
    unit: str
    unit_Bprice: float  # buying price per unit
    unit_Sprice: float  #selling price per unit
    supplier: str  # Supplier name
    min_stock:float
    last_updated: datetime = datetime.utcnow()

class House(BaseModel):
    house_number: str
    fixed_rent: float
    tenant_name:Optional[str]=None
