"""
Database connection and utility functions.

This module provides database connection management and helper functions
for interacting with the SQLite database.
"""
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Optional, List, Dict, Any
from config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    """
    Create and return a database connection.
    
    Returns:
        sqlite3.Connection: A connection to the SQLite database with
                           row factory set to return dict-like rows.
    """
    connection = sqlite3.connect(str(DATABASE_PATH))
    connection.row_factory = sqlite3.Row
    return connection


def get_all_books() -> List[Dict[str, Any]]:
    """
    Retrieve all books from the database.
    
    Returns:
        List[Dict[str, Any]]: List of book dictionaries with all fields.
    """
    with closing(get_connection()) as connection:
        cursor = connection.execute("SELECT * FROM books")
        return [dict(row) for row in cursor.fetchall()]


def get_customer(customer_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a customer by ID.
    
    Args:
        customer_id: The unique identifier of the customer.
        
    Returns:
        Optional[Dict[str, Any]]: Customer dictionary if found, None otherwise.
    """
    with closing(get_connection()) as connection:
        cursor = connection.execute(
            "SELECT * FROM customers WHERE id = ?",
            (customer_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def update_stock(isbn: str, quantity: int) -> None:
    """
    Update the stock quantity for a book.
    
    Args:
        isbn: The ISBN of the book to update.
        quantity: The new stock quantity.
    """
    with closing(get_connection()) as connection:
        connection.execute(
            "UPDATE books SET stock = ? WHERE isbn = ?",
            (quantity, isbn)
        )
        connection.commit()


if __name__ == "__main__":
    """Test database connection and functions."""
    books = get_all_books()
    for book in books:
        print(f"{book['title']}: {book['stock']} in stock")
