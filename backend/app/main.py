from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.database import products_collection  # Import from database.py
from app.database import db  # Import database connection
from app.routes.cyber import router as cyber_router
from app.routes.shop import router as shop_router
from app.routes.property import router as rental_router
from app.routes.gas import router as gas_router
from app.routes import property

app = FastAPI(title="Multi-Business Management API")

app.include_router(shop_router)
app.include_router(cyber_router)
app.include_router(rental_router)
app.include_router(gas_router)
app.include_router(property.router)

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update if using a different frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/products", response_model=List[str])
async def get_products():
    products = products_collection.find({}, {"_id": 0, "name": 1})  # Fetch only product names
    return [product["name"] for product in products]

@app.get("/")
async def home():
    return {"message": "Welcome to the Multi-Business API"}

@app.get("/test-db")
async def test_db():
    collections = await db.list_collection_names()
    return {"collections": collections}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
