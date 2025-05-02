# farmer service business logic
import uuid
from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException, status
from app.db.connection import get_db_connection
from app.auth.jwt_handler import create_access_token
from app.auth.password_utils import hash_password, validate_password_strength, verify_password

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
    def add_products(self, farmer_id, product_name, product_category, quantity, date=datetime.now()):
        # method to add a product(s) to the database
        # product must have a product id
        product_id = str(uuid.uuid4())[:5]

        #check if product already exists, if yes then only add its quantity
        self.cursor.execute("SELECT product_id FROM products WHERE farmer_id = %s", (farmer_id,))
        if self.cursor.fetchone():


    #def add_product(self, farmer_id, product_name, product_category, quantity, date=datetime.now):
    #    # method to add a product(s) to the database
    #    # product must have a product id
    #    try:
    #        connection = get_db_connection()
    #        cursor = connection.cursor()
    #        
    #        connection.autocommit = False
#
    #        self.cursor.execute(
    #            "INSERT INTO products (farmer_id, product_name, product_category, quantity, date)",
    #            (farmer_id, product_name, product_category, quantity, date)
    #        )
    #        self.connection.commit()
    #    except Exception as e:
    #        self.conn.rollback()
    #        raise HTTPException(
    #            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #            details=f"Error adding products to the database! {str(e)}"
    #        )
#
    #    finally:
    #        self._cleanup()




    def _cleanup(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

