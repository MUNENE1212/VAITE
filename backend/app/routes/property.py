from fastapi import APIRouter, HTTPException
from app.database import db
from datetime import datetime
from pydantic import Field
from app.models import RentalPayment
from app.crud import House
from bson import ObjectId

router = APIRouter(prefix="/rental", tags=["Rental Management"])

# Converter function to handle ObjectId serialization
def convert_object_id(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, list):
        return [convert_object_id(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_object_id(value) for key, value in obj.items()}
    return obj

@router.post("/property/rent/payment", operation_id="process_rent_payment_entry")
async def pay_rent_payment(payment: RentalPayment):
    # Get the fixed rent for the house
    house_data = await db.houses.find_one({"house_number": payment.house_number})
    if not house_data:
        raise HTTPException(status_code=404, detail="House not found")

    fixed_rent = house_data.get("fixed_rent")
    if payment.amount_paid != fixed_rent:
        raise HTTPException(status_code=400, detail=f"Incorrect rent amount. Expected {fixed_rent}")

    # Save valid rent payment
    rent_record = {
        "tenant_name": payment.tenant_name,
        "house_number": payment.house_number,
        "amount_paid": payment.amount_paid,
        "month": payment.month,
        "water_bill": payment.water_bill,
        "electricity_bill": payment.electricity_bill,
        "timestamp": payment.timestamp
    }

    await db.rent_payments.insert_one(rent_record)

    return {"message": "Rent payment recorded successfully", "data": convert_object_id(rent_record)}

@router.post("/property/houses/add", operation_id="register_new_house_entry")
async def add_house_route(house: House):
    # Check if house exists
    existing_house = await db.houses.find_one({"house_number": house.house_number})
    if existing_house:
        raise HTTPException(status_code=400, detail="House already exists")

    # Insert new house
    await db.houses.insert_one(house.dict())
    return {"message": "House added successfully", "house": convert_object_id(house.dict())}

@router.get("/property/houses/status", operation_id="fetch_houses_status")
async def get_houses_status():
    # Fetch all houses
    houses_cursor = db.houses.find({})
    houses = await houses_cursor.to_list(length=None)

    if not houses:
        raise HTTPException(status_code=404, detail="No houses found")

    # Fetch rent payments for the current month
    current_month = datetime.utcnow().strftime("%B")  # Example: "February"
    rent_payments = await db.rent_payments.find({"month": current_month}).to_list(length=None)

    # Create a mapping of paid houses
    paid_houses = {payment["house_number"]: payment for payment in rent_payments}

    # Process house data
    house_status_list = []
    for house in houses:
        house_number = house["house_number"]
        status = "Paid" if house_number in paid_houses else "Pending"

        house_status_list.append({
            "house_number": house_number,
            "fixed_rent": house["fixed_rent"],
            "status": status
        })

    return {"houses": convert_object_id(house_status_list)}
