# Email Notification Service
import smtplib
import os
import asyncpg
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)
load_dotenv()

class EmailNotifications:
    def __init__(self, db_pool: asyncpg.pool.Pool):
        load_dotenv()
        """Initializes with smtp server details
        Args:
            smtp_host (str): The smtp server host
            smtp_port (str): The smtp server port
            smtp_user (str): The sender's email address
            smtp_password (str): Sender's email password or app-specific password"""
        
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.db_pool = db_pool

    def send_email(self, recipient_email: str, subject: str, body: str):
        #Internal helper to send an email via SMTP
        msg = MIMEMultipart()
        msg["From"] = self.smtp_user
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, recipient_email, msg.as_string())
            logger.info(f"Email successfully sent to {recipient_email}")
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")
            raise

    async def send_order_receipt(self, order_id: int):
        """
        Fetches order details + items from DB and sends an order receipt email.
        """
        async with self.db_pool.acquire() as conn:
            # Fetch order header
            order = await conn.fetchrow("""
                SELECT o.id, o.total_amount, b.first_name AS buyer_name, b.email AS buyer_email
                FROM orders o
                JOIN buyers b ON o.buyer_id = b.id
                WHERE o.id = $1
            """, order_id)

            if not order:
                logger.warning(f"No order found with ID {order_id}")
                return

            # Fetch order items
            order_items_rows = await conn.fetch("""
                SELECT oi.user_id, oi.product_id, oi.quantity, p.price AS unit_price,
                       (oi.quantity * p.price) AS total_price,
                       p.farmer_id, p.date_time AS order_date
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = $1
            """, order_id)

        # Convert rows to list of dicts matching the structure
        order_items = []
        for row in order_items_rows:
            order_items.append({
                "user_id": row["user_id"],
                "product_id": row["product_id"],
                "quantity": row["quantity"],
                "unit_price": row["unit_price"],
                "total_price": row["total_price"],
                "farmer_id": row["farmer_id"],
                "order_date": row["order_date"]
            })

        # Build the email body
        items_str = "\n".join([
            f"- Product {item['product_id']} (Qty: {item['quantity']}, "
            f"Unit: ${item['unit_price']}, Total: ${item['total_price']})"
            for item in order_items
        ])

        body = (
            f"Hello {order['buyer_name']},\n\n"
            f"Thank you for your purchase!\n\n"
            f"Order ID: {order['id']}\n"
            f"Total Amount: ${order['total_amount']}\n\n"
            f"Items:\n{items_str}\n\n"
            f"We appreciate your support.\n\n"
            f"Best regards,\nFarmer's Market"
        )

        self.send_email(order["buyer_email"], "Your Order Receipt", body)

    async def send_order_request(self, order_id: int, farmer_id: int, send_email_func):
        async with self.db_pool.acquire() as conn:
            # Fetch buyer and order info for this farmer's items
            order = await conn.fetchrow("""
                SELECT o.id AS order_id,
                       o.date_time AS order_date,
                       b.first_name AS buyer_name,
                       b.email AS buyer_email,
                       SUM(oi.quantity * p.price) AS total_amount
                FROM orders o
                JOIN order_items oi ON o.id = oi.order_id
                JOIN products p ON oi.product_id = p.id
                JOIN buyers b ON o.buyer_id = b.id
                WHERE o.id = $1
                  AND p.farmer_id = $2
                GROUP BY o.id, o.date_time, b.first_name, b.email
            """, order_id, farmer_id)

            if not order:
                logger.warning(f"No order found for farmer_id={farmer_id} in order_id={order_id}")
                return

            # Fetch only this farmer's order items
            order_items_rows = await conn.fetch("""
                SELECT p.name AS product_name,
                       oi.quantity,
                       p.price AS unit_price,
                       (oi.quantity * p.price) AS total_price
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = $1
                  AND p.farmer_id = $2
            """, order_id, farmer_id)

            # Build email body
            email_body = f"New Order #{order['order_id']} from {order['buyer_name']} on {order['order_date']}\n\n"
            for item in order_items_rows:
                email_body += f"- {item['product_name']} (x{item['quantity']}): ${item['total_price']:.2f}\n"

            email_body += f"\nTotal: ${order['total_amount']:.2f}"

            # Fetch farmer's email
            farmer_email = await conn.fetchval("SELECT email FROM farmers WHERE id = $1", farmer_id)
            if not farmer_email:
                logger.warning(f"No email found for farmer_id={farmer_id}")
                return

            # Send the email
            await self.send_email(
                to=farmer_email,
                subject=f"New Order #{order['order_id']}",
                body=email_body
            )
            
            