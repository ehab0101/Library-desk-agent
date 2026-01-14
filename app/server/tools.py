from typing import List, Dict, Any, Optional, Union
from langchain.tools import tool
from db import get_connection
from config import VALID_SEARCH_FIELDS, LOW_STOCK_THRESHOLD


@tool
def find_books(q: str, by: str) -> List[Dict[str, Any]]:
    if by not in VALID_SEARCH_FIELDS:
        return []
    
    search_query = f"%{q}%"
    select_fields = "isbn, title, author, price, stock"
    
    with get_connection() as connection:
        sql_query = f"SELECT {select_fields} FROM books WHERE {by} LIKE ?"
        cursor = connection.execute(sql_query, (search_query,))
        return [dict(row) for row in cursor.fetchall()]


@tool
def create_order(customer_id: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not items:
        raise ValueError("Order must contain at least one item")
    
    with get_connection() as connection:
        cursor = connection.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO orders (customer_id) VALUES (?)",
                (customer_id,)
            )
            order_id = cursor.lastrowid
            
            for item in items:
                isbn = item.get("isbn")
                quantity = item.get("qty")
                
                if not isbn or quantity is None:
                    raise ValueError(f"Invalid item: {item}")
                
                cursor.execute(
                    "INSERT INTO order_items (order_id, isbn, qty) VALUES (?, ?, ?)",
                    (order_id, isbn, quantity)
                )
                
                cursor.execute(
                    "UPDATE books SET stock = stock - ? WHERE isbn = ?",
                    (quantity, isbn)
                )
            
            connection.commit()
            
            return {
                "order_id": order_id,
                "status": "created"
            }
        except Exception as error:
            connection.rollback()
            raise ValueError(f"Failed to create order: {str(error)}") from error


@tool
def restock_book(isbn: str, quantity: int) -> Dict[str, Any]:
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    
    with get_connection() as connection:
        connection.execute(
            "UPDATE books SET stock = stock + ? WHERE isbn = ?",
            (quantity, isbn)
        )
        connection.commit()
    
    return {"isbn": isbn, "added": quantity}


@tool
def update_price(isbn: str, price: float) -> Dict[str, Any]:
    if price <= 0:
        raise ValueError("Price must be positive")
    
    with get_connection() as connection:
        connection.execute(
            "UPDATE books SET price = ? WHERE isbn = ?",
            (price, isbn)
        )
        connection.commit()
    
    return {"isbn": isbn, "new_price": price}


@tool
def order_status(order_id: int) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    order_query = """
        SELECT o.id AS order_id,
               c.name AS customer,
               b.title,
               oi.qty
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        JOIN order_items oi ON o.id = oi.order_id
        JOIN books b ON oi.isbn = b.isbn
        WHERE o.id = ?
    """
    
    with get_connection() as connection:
        cursor = connection.execute(order_query, (order_id,))
        rows = cursor.fetchall()
    
    if not rows:
        return {"error": "Order not found"}
    
    return [dict(row) for row in rows]


@tool
def inventory_summary() -> List[Dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT title, stock FROM books WHERE stock < ?",
            (LOW_STOCK_THRESHOLD,)
        )
        return [dict(row) for row in cursor.fetchall()]
