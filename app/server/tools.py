"""
Library management tools for database operations.

This module provides Langchain tools that interact with the database
to perform various library management operations.
"""
from typing import List, Dict, Any, Optional, Union
from langchain.tools import tool
from db import get_connection
from config import VALID_SEARCH_FIELDS, LOW_STOCK_THRESHOLD


@tool
def find_books(q: str, by: str) -> List[Dict[str, Any]]:
    """
    Search for books by title or author.
    
    Args:
        q: The search query string.
        by: Field to search by - must be 'title' or 'author'.
        
    Returns:
        List[Dict[str, Any]]: List of matching books with ISBN, title, author, price, and stock.
                              Returns empty list if by is invalid.
    """
    if by not in VALID_SEARCH_FIELDS:
        return []
    
    search_query = f"%{q}%"
    select_fields = "isbn, title, author, price, stock"
    
    with get_connection() as connection:
        # Using parameterized query to prevent SQL injection
        # Note: Field name is validated above, so this is safe
        sql_query = f"SELECT {select_fields} FROM books WHERE {by} LIKE ?"
        cursor = connection.execute(sql_query, (search_query,))
        return [dict(row) for row in cursor.fetchall()]


@tool
def create_order(customer_id: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create a new order and automatically reduce book stock.
    
    Args:
        customer_id: The ID of the customer placing the order.
        items: List of order items, each containing 'isbn' and 'qty'.
        
    Returns:
        Dict[str, Any]: Dictionary containing 'order_id' and 'status'.
        
    Raises:
        ValueError: If items list is empty or invalid.
    """
    if not items:
        raise ValueError("Order must contain at least one item")
    
    with get_connection() as connection:
        cursor = connection.cursor()
        
        try:
            # Create order record
            cursor.execute(
                "INSERT INTO orders (customer_id) VALUES (?)",
                (customer_id,)
            )
            order_id = cursor.lastrowid
            
            # Process each order item
            for item in items:
                isbn = item.get("isbn")
                quantity = item.get("qty")
                
                if not isbn or quantity is None:
                    raise ValueError(f"Invalid item: {item}")
                
                # Insert order item
                cursor.execute(
                    "INSERT INTO order_items (order_id, isbn, qty) VALUES (?, ?, ?)",
                    (order_id, isbn, quantity)
                )
                
                # Update book stock
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
    """
    Increase the stock quantity of a book.
    
    Args:
        isbn: The ISBN of the book to restock.
        quantity: The quantity to add to current stock.
        
    Returns:
        Dict[str, Any]: Dictionary containing 'isbn' and 'added' quantity.
    """
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
    """
    Update the price of a book.
    
    Args:
        isbn: The ISBN of the book to update.
        price: The new price (must be positive).
        
    Returns:
        Dict[str, Any]: Dictionary containing 'isbn' and 'new_price'.
    """
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
    """
    Retrieve detailed information about a specific order.
    
    Args:
        order_id: The unique identifier of the order.
        
    Returns:
        Dict[str, Any] | List[Dict[str, Any]]: Order details with customer and items,
                                                 or error dict if not found.
    """
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
    """
    Retrieve a list of books with low stock levels.
    
    Returns:
        List[Dict[str, Any]]: List of books with 'title' and 'stock' fields
                              where stock is below the threshold.
    """
    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT title, stock FROM books WHERE stock < ?",
            (LOW_STOCK_THRESHOLD,)
        )
        return [dict(row) for row in cursor.fetchall()]
