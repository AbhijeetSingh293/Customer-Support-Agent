from langchain_core.tools import tool
from .mock_data import MOCK_PRODUCTS

@tool
def check_product_availability(product_name: str) -> str:
    """Check stock and pricing for a product."""
    for prod_id, details in MOCK_PRODUCTS.items():
        if product_name.lower() in details["name"].lower():
            stock = "In Stock" if details["in_stock"] else "Out of Stock"
            return f"{details['name']}: Price {details['price']}, Status: {stock}"
    return f"Product '{product_name}' was not found in the catalog."