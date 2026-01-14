from google.genai import types
from typing import List


def create_find_books_declaration() -> types.FunctionDeclaration:
    return types.FunctionDeclaration(
        name="find_books",
        description=(
            "Find books by title or author. Returns a list of matching books "
            "with ISBN, title, author, price, and stock."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "q": types.Schema(
                    type="STRING",
                    description="Search query string"
                ),
                "by": types.Schema(
                    type="STRING",
                    description="Search by 'title' or 'author'",
                    enum=["title", "author"]
                )
            },
            required=["q", "by"]
        )
    )


def create_create_order_declaration() -> types.FunctionDeclaration:
    return types.FunctionDeclaration(
        name="create_order",
        description=(
            "Create a new order for a customer and reduce book stock. "
            "Returns order_id and status."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "customer_id": types.Schema(
                    type="INTEGER",
                    description="Customer ID"
                ),
                "items": types.Schema(
                    type="ARRAY",
                    description="List of order items",
                    items=types.Schema(
                        type="OBJECT",
                        properties={
                            "isbn": types.Schema(
                                type="STRING",
                                description="Book ISBN"
                            ),
                            "qty": types.Schema(
                                type="INTEGER",
                                description="Quantity"
                            )
                        },
                        required=["isbn", "qty"]
                    )
                )
            },
            required=["customer_id", "items"]
        )
    )


def create_restock_book_declaration() -> types.FunctionDeclaration:
    return types.FunctionDeclaration(
        name="restock_book",
        description=(
            "Increase book stock by a specified quantity. "
            "Returns ISBN and quantity added."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "isbn": types.Schema(
                    type="STRING",
                    description="Book ISBN"
                ),
                "qty": types.Schema(
                    type="INTEGER",
                    description="Quantity to add to stock"
                )
            },
            required=["isbn", "qty"]
        )
    )


def create_update_price_declaration() -> types.FunctionDeclaration:
    return types.FunctionDeclaration(
        name="update_price",
        description="Update the price of a book. Returns ISBN and new price.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "isbn": types.Schema(
                    type="STRING",
                    description="Book ISBN"
                ),
                "price": types.Schema(
                    type="NUMBER",
                    description="New price"
                )
            },
            required=["isbn", "price"]
        )
    )


def create_order_status_declaration() -> types.FunctionDeclaration:
    return types.FunctionDeclaration(
        name="order_status",
        description=(
            "Get order details including customer name, book titles, and quantities. "
            "Returns order information or error if not found."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "order_id": types.Schema(
                    type="INTEGER",
                    description="Order ID"
                )
            },
            required=["order_id"]
        )
    )


def create_inventory_summary_declaration() -> types.FunctionDeclaration:
    return types.FunctionDeclaration(
        name="inventory_summary",
        description=(
            "List all books with low stock (stock < 5). "
            "Returns list of books with title and stock."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={},
            required=[]
        )
    )


def get_all_tool_declarations() -> List[types.FunctionDeclaration]:
    return [
        create_find_books_declaration(),
        create_create_order_declaration(),
        create_restock_book_declaration(),
        create_update_price_declaration(),
        create_order_status_declaration(),
        create_inventory_summary_declaration(),
    ]
