# FAST API entry

import asyncpg
from fastapi import FastAPI
from app.api.routes import users, farmers, products, orders

app = FastAPI(title = "Farm-Client API (RAW SQL)")

app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(farmers.router, prefix="/api/farmers", tags=["Farmers"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])

app.state.db_pool = None

@app.on_event("startup")
async def startup():
    app.state.db_pool = await asyncpg.create_pool(
        user="postgres", password="pass", database="mydb", host="localhost"
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.db_pool.close()