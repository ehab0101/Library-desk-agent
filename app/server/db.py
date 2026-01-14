import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Optional, List, Dict, Any
from config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(str(DATABASE_PATH))
    connection.row_factory = sqlite3.Row
    return connection


def get_all_books() -> List[Dict[str, Any]]:
    with closing(get_connection()) as connection:
        cursor = connection.execute("SELECT * FROM books")
        return [dict(row) for row in cursor.fetchall()]


def get_customer(customer_id: int) -> Optional[Dict[str, Any]]:
    with closing(get_connection()) as connection:
        cursor = connection.execute(
            "SELECT * FROM customers WHERE id = ?",
            (customer_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def update_stock(isbn: str, quantity: int) -> None:
    with closing(get_connection()) as connection:
        connection.execute(
            "UPDATE books SET stock = ? WHERE isbn = ?",
            (quantity, isbn)
        )
        connection.commit()


if __name__ == "__main__":
    books = get_all_books()
    for book in books:
        print(f"{book['title']}: {book['stock']} in stock")
