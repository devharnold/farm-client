# order service business logic
import uuid
from uuid import uuid4
import logging
from datetime import datetime
from fastapi import HTTPException, status
from app.db.connection import get_db_connection

logging.basicConfig(level=logging.INFO)

class OrderService:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    def add_order(self, product_id, name, quantity):
        # method to add an order, can be a normal user, admin or even the farmer
        # first pull products from the products table
        