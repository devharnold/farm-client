import uuid
import logging
import asyncpg
from datetime import datetime
from fastapi import HTTPException, status
from app.db import get_db_pool

logging.basicConfig(level=logging.INFO)

class ProductService:
    def __init__(self, db_pool: asyncpg.pool.Pool):
        self.db_pool = db_pool

    async def add_products(self, farmer_id, name, category, quantity, price,
                           created_at=None, updated_at=None):
        created_at = created_at or datetime.now()
        updated_at = updated_at or datetime.now()

        async with self.db_pool.acquire() as conn:
            product = await conn.fetchrow(
                """
                SELECT product_id, quantity FROM products
                WHERE farmer_id = $1 AND name = $2 AND category = $3
                """,
                farmer_id, name, category
            )

            if product:
                new_quantity = product["quantity"] + quantity
                await conn.execute(
                    """
                    UPDATE products SET quantity = $1, created_at = $2
                    WHERE product_id = $3
                    """,
                    new_quantity, created_at, product["product_id"]
                )
            else:
                product_id = str(uuid.uuid4())[:5]
                await conn.execute(
                    """
                    INSERT INTO products (product_id, farmer_id, name, category,
                    quantity, price, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    """,
                    product_id, farmer_id, name, category,
                    quantity, price, created_at, updated_at
                )

    async def check_if_product_exists(self, product_id):
        # checks if a certain product already exists in your database
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchval(
                "SELECT COUNT(*) FROM products WHERE product_id = $1", product_id
            )
            return result > 0

    async def delete_product(self, product_id):
        # deletes the product entirely from the database, can be inserted again
        try:
            if not await self.check_if_product_exists(product_id):
                logging.warning("Product does not exist")
                return

            async with self.db_pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        "DELETE FROM products WHERE product_id = $1", product_id
                    )
                    logging.info(f"Product {product_id} has been deleted!")

        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to delete product")

    async def reset_product_quantity(self, product_id):
        # a farmer may want to clear stock, so we give the soft-delete option
        try:
            if not await self.check_if_product_exists(product_id):
                print(f"Product {product_id} does not exist")
                return

            async with self.db_pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        "UPDATE products SET quantity = 0 WHERE product_id = $1", product_id
                    )
                    print(f"You have reset the product's {product_id} quantity to 0")
        except Exception as e:
            print(f"Error {str(e)}")