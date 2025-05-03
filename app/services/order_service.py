# order service business logic
import uuid
from uuid import uuid4
import logging
import asyncpg
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from app.db import get_db_pool

logging.basicConfig(level=logging.INFO)

class OrderService:
    def __init__(self, db_pool: asyncpg.pool.Pool):
        self.db_pool = db_pool

    async def create_orders(self, buyer_id: int, items: List[dict], delivery_address: str = ""):
        order_id = str(uuid.uuid4())[:5]
        if not items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No items provided"
            )
        async with self.db_pool.acquire() as conn:
            total_price = 0.0
            order_items = []

            for item in items:
                product_id = item["product_id"]
                quantity = item["quantity"]

                product = await conn.fetchrow(
                    "SELECT stock, price, farmer_id, FROM products WHERE product_id = $1",
                    product_id
                )
                if not product:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product not found"
                    )
                if product["stock"] < quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Not enough stock for product {product_id}"
                    )
                
                item_total = quantity * product(product_id)
                total_price += item_total

                order_items.append({
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": product["price"],
                    "total_price": item_total,
                    "farmer_id": product["farmer_id"]
                })

            order_row = await conn.fetchrow(
                """INSERT INTO orders (user_id, total_price, delivery_address, payment_method, status, order_date)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id
                """, buyer_id, total_price, delivery_address, payment_method, datetime.now()
            )
            order_id = order_row["id"]

            for items in order_items:
                await conn.execute(
                    """INSERT INTO order_items (order_id, product_id, farmer_id, quantity, unit_price, total_price)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """, order_id, item["product_id"], item["farmer_id"], item["quantity"], item["unit_price"], item["total_price"]
                )

                await conn.execute(
                    "UPDATE products SET stock = stock - $1 WHERE id = $2",
                    item["quantity"], item["product_id"]
                )

            return {"order_id": order_id, "message": "Order places successfully"}
        
    async def view_requests(self, user_id, items: List[dict]):
        pass