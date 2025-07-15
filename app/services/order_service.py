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

    async def create_orders(self, buyer_id: int, items: List[dict], delivery_address: str = "", date_created=datetime.now()):
        #this will be for a normal user
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
                    "farmer_id": product["farmer_id"],
                    "order_date": product["date_time"]
                })

            order_row = await conn.fetchrow(
                """INSERT INTO orders (user_id, total_price, delivery_address, payment_method, status, order_date)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id
                """, buyer_id, total_price, delivery_address, payment_method, date_created
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
        
    async def remove_item(self, order_id, user_id, items: List[dict], date_removed=datetime.now()):
        # remove items/ an item from the orders list
        async with self.db_pool.acquire() as conn:
            order_list = []
            for item in items:
                product_id = item["product_id"]
                quantity = item["quantity"]
                
                

        
    async def view_cart(self, order_id, items: List[dict], date_created=datetime.now()):
        # view cart -> for a normal user's dashboard
        with self.db_pool.acquire() as conn:
            # fetch a list of requests first
            requested_items = []
            for item in items:
                product_id = item["product_id"]
                quantity = item["quantity"]
                unit_price = item["unit_price"]
                total_price = item["total_price"]
                farmer_id = item["farmer_id"]
                date_created = item["date_created"]
                orders = await conn.fetchrow(
                    "SELECT COUNT (*) FROM order_list WHERE order_id = $1",
                    order_id
                )
                if not orders:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Orders not found!"
                    )
                
                return requested_items.append({
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "total_price": total_price,
                    "farmer_id": farmer_id,
                    "date_created": date_created
                })
            
    async def view_orders(self, user_id, order_id, items: List[dict], date_created=datetime.now()):
        # farmer views the requested orders from a specific user
        with self.db_pool.acquire() as conn:
            ordered_items = []
            for item in items:
                product_id = item["product_id"]
                quantity = item["quantity"]
                unit_price = item["unit_price"]
                total_price = item["total_price"]
                user_id = item["user_id"]
                date_created = item["date"]
                orders = await conn.fetrow(
                    "SELECT COUNT(*) FROM orders WHERE order_id = $1",
                    (order_id)
                )
                if not orders:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Order cannot be traced"
                    )
                
                return ordered_items.append({
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "total_price": total_price,
                    "user_id": user_id,
                    "date": date_created
                })

