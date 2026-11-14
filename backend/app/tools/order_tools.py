from langchain_core.tools import tool
from .mock_data import MOCK_ORDERS

@tool
def track_order(order_id: str) -> str:
    """Look up order delivery status and details by order ID."""
    order = MOCK_ORDERS.get(order_id.strip().upper())
    if not order:
        return f"Order {order_id} not found."
    return f"Order {order_id}: Item: {order['item']}, Status: {order['status']}, Expected Delivery: {order['delivery_date']}"