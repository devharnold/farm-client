# farmer service business logic
import uuid
from uuid import uuid4
import logging
from datetime import datetime
from fastapi import HTTPException, status
from app.db.connection import get_db_connection
from app.auth.jwt_handler import create_access_token
from app.auth.password_utils import hash_password, validate_password_strength, verify_password

logging.basicConfig(level=logging.INFO)

class FarmerService:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    def register_farmer(self, email: str, password: str, username: str, role: str):
        # Generate farmer_id
        farmer_id = str(uuid.uuid4())[:8]
        hashed_password = hash_password(password)

        # Check password strength
        if not validate_password_strength(password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password strength is too weak"
            )
        
        # Check if the farmer already exists in the database
        self.cursor.execute("SELECT id FROM farmers WHERE email = %s AND username = %s", (email, username))
        if self.cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Farmer with this email or username already exists"
            )
        
        try:
            # Insert the farmer into the database
            self.cursor.execute(
                "INSERT INTO farmers (id, username, email, password, role)",
                (farmer_id, username, email, hashed_password, role)
            )
            farmer_id = self.cursor.fetchone()[0]
            self.conn.commit()

            return {"message": "Farmer registered successfully", "farmer_id": farmer_id}
        
        except Exception as e:
            self.conn.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while registering the user: {str(e)}"
            )
        finally:
            self._cleanup()

    def farmer_login(self, email: str, password: str):
        # method to log in the farmer to the system
        try:
            self.cursor.execute(
                "SELECT id, password FROM farmers WHERE email = %s", (email,)
            )
            farmer = self.cursor.fetchone()

            if not farmer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            farmer_id, hashed_password = farmer

            if not verify_password(password, hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password"
                )
            token = create_access_token({"farmer_id": farmer_id})
            return {"access_token": token}
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Login failed: {str(e)}"
            )
        finally:
            self._cleanup()

    def add_products(self, farmer_id, name, category, quantity, price, created_at=datetime.now(), updated_at=datetime.now()):
        # check if product exists
        self.cursor.execute(
            "SELECT product_id, quantity FROM products WHERE farmer_id = %s AND name = %s AND category = %s",
            (farmer_id, name, category)
        )
        existing_product = self.cursor.fetchone()

        if existing_product:
            # this means that the product exists therefore update its quantity
            product_id, current_quantity = existing_product
            new_quantity = current_quantity + quantity # add the new quantity to the existing one
            self.cursor.execute(
                "UPDATE products SET quantity = %s, created_at = %s WHERE product_id = %s",
                (new_quantity, created_at, product_id)
            )
        else:
            # product doesn't exist, insert a new one
            product_id = str(uuid.uuid4())[:5]
            self.cursor.execute(
                "INSERT INTO products (product_id, farmer_id, name, category, quantity, price, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (product_id, farmer_id, name, category, quantity, price, created_at, updated_at)
            )

        self._cleanup()

    def check_if_product_exists(self, product_id):
        self.cursor.execute(
            "SELECT COUNT(*) FROM products WHERE product_id = %s;", (product_id,)
        )
        result = self.cursor.fetchone()
        return result[0] > (0) # True if product exists, result[0] contains the count returned by the query which is a number
    
    def delete_product(self, product_id):
        try:
            # first check if product exists
            if not self.check_if_product_exists(product_id):
                logging.warning(f"Product does not exist")
                return # Exit if product doesn't exist

            # start the transaction
            self.cursor.execute("BEGIN;")

            self.cursor.execute(
                "DELETE from products WHERE product_id = %s", (product_id,)
            )

            # commit the transaction
            self.conn.commit()

            logging.info(f"Product {product_id} has been deleted!")

        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error: {str(e)}")

    def reset_product_quantity(self, product_id):
        # method to delete a product
        # first check if the product exists
        try:
            if not self.check_if_product_exists(product_id):
                print(f"Product {product_id} does not exist")
                return # Exit if the product does not exist
            
            self.cursor.execute("BEGIN;")

            self.cursor.execute(
                "UPDATE products SET quantity = 0 WHERE product_id = %s;", (product_id,)
            )

            # commit the transaction
            self.conn.commit()

            print(f"You have reset the product's {product_id} quantity to 0")
            
        except Exception as e:
            self.conn.rollback()
            print(f"Error {str(e)}")

    def _cleanup(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()