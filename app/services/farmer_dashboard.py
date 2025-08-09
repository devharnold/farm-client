# Farmer dashboard

"""This dashboard is aimed to help the farmer see the notifications
And also view the number of orders the respective has received
The farmer should also be able to tick off items from the dashboard
After the orders have been settled
"""

import asyncpg
import os
import logging
from typing import List
from datetime import datetime
from app.services.order_service import OrderService
from app.services.user_service import UserService

logging.basicConfig(level=logging.INFO)

class FarmerDashboard:
    def __init__(self, db_pool: asyncpg.pool.Pool):
        self.db_pool = db_pool

    async def display_order_items(self, farmer_id: int, page: int = 1, limit: int = 10) -> List[dict]:
        # Calculate offset from page number
        offset = (page - 1) * limit

        async with self.db_pool.acquire() as conn:
            order_list = await conn.fetch("""
                SELECT o.id AS order_id,
                       o.date_time AS order_date,
                       oi.user_id AS buyer_id,
                       SUM(oi.quantity * p.price) AS total_amount,
                       COUNT(DISTINCT oi.product_id) AS total_items
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                JOIN orders o ON oi.order_id = o.id
                WHERE p.farmer_id = $1
                GROUP BY o.id, o.date_time, oi.user_id
                ORDER BY o.date_time DESC
                LIMIT $2 OFFSET $3
            """, farmer_id, limit, offset)

            return [dict(order) for order in order_list]
