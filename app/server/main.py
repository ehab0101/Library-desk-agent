"""
Flask REST API server for Library Desk Agent.

This module provides HTTP endpoints for the chat interface,
session management, and order viewing.
"""
import os
from typing import Dict, Any, Tuple
from flask import Flask, request, jsonify
from flask_cors import CORS

from dotenv import load_dotenv
from agent import library_agent
from models import (
    save_message,
    get_session_messages,
    get_sessions
)
from db import get_connection
from contextlib import closing
from config import (
    DEFAULT_SESSION_ID,
    CONVERSATION_HISTORY_LIMIT,
    DEFAULT_PORT,
    DEFAULT_HOST
)


load_dotenv()
app = Flask(__name__)
CORS(app)


def _build_error_response(error_message: str, status_code: int = 500) -> tuple[Dict[str, str], int]:
    """
    Build a standardized error response.
    
    Args:
        error_message: Error message string.
        status_code: HTTP status code.
        
    Returns:
        Tuple of (JSON response, status code).
    """
    return jsonify({'error': error_message}), status_code


def _build_success_response(data: Dict[str, Any], status_code: int = 200) -> Tuple[Dict[str, Any], int]:
    """
    Build a standardized success response.
    
    Args:
        data: Response data dictionary.
        status_code: HTTP status code.
        
    Returns:
        Tuple of (JSON response, status code).
    """
    return jsonify(data), status_code


@app.route('/api/chat', methods=['POST'])
def handle_chat() -> tuple[Dict[str, Any], int]:
    """
    Handle chat messages from the frontend.
    
    Request body:
        {
            "message": str,
            "session_id": str (optional, defaults to "default")
        }
    
    Returns:
        JSON response with agent reply and session_id.
    """
    try:
        request_data = request.json or {}
        message = request_data.get('message', '').strip()
        session_id = request_data.get('session_id', DEFAULT_SESSION_ID)
        
        if not message:
            return _build_error_response('Message is required', 400)
        
        # Load conversation history for context
        previous_messages = get_session_messages(session_id)
        conversation_history = [
            {"role": msg['role'], "content": msg['content']}
            for msg in previous_messages[-CONVERSATION_HISTORY_LIMIT:]
        ]
        
        # Save user message
        save_message(session_id, 'user', message)
        
        # Get agent response
        agent_response = library_agent(message, session_id, conversation_history)
        
        # Save assistant response
        save_message(session_id, 'assistant', agent_response)
        
        return _build_success_response({
            'response': agent_response,
            'session_id': session_id
        })
    
    except Exception as error:
        return _build_error_response(str(error), 500)


@app.route('/api/sessions', methods=['GET'])
def handle_get_sessions() -> Tuple[Dict[str, Any], int]:
    """
    Get list of all chat sessions.
    
    Returns:
        JSON response with list of session IDs.
    """
    try:
        sessions = get_sessions()
        return _build_success_response({'sessions': sessions})
    except Exception as error:
        return _build_error_response(str(error), 500)


@app.route('/api/sessions/<session_id>/messages', methods=['GET'])
def handle_get_messages(session_id: str) -> Tuple[Dict[str, Any], int]:
    """
    Get all messages for a specific session.
    
    Args:
        session_id: The session identifier.
        
    Returns:
        JSON response with list of messages.
    """
    try:
        messages = get_session_messages(session_id)
        return _build_success_response({'messages': messages})
    except Exception as error:
        return _build_error_response(str(error), 500)


@app.route('/api/health', methods=['GET'])
def handle_health_check() -> Tuple[Dict[str, str], int]:
    """
    Health check endpoint.
    
    Returns:
        JSON response indicating server status.
    """
    return _build_success_response({'status': 'ok'})


@app.route('/api/orders', methods=['GET'])
def handle_get_orders() -> Tuple[Dict[str, Any], int]:
    """
    Get all orders with customer and item details.
    
    Returns:
        JSON response with list of orders.
    """
    try:
        orders_query = """
            SELECT 
                o.id AS order_id,
                o.customer_id,
                c.name AS customer_name,
                c.email AS customer_email,
                o.created_at,
                GROUP_CONCAT(
                    b.title || ' (x' || oi.qty || ')', 
                    ', '
                ) AS items
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            LEFT JOIN order_items oi ON o.id = oi.order_id
            LEFT JOIN books b ON oi.isbn = b.isbn
            GROUP BY o.id, o.customer_id, c.name, c.email, o.created_at
            ORDER BY o.id DESC
        """
        
        with closing(get_connection()) as connection:
            cursor = connection.execute(orders_query)
            orders = [
                {
                    'order_id': row['order_id'],
                    'customer_id': row['customer_id'],
                    'customer_name': row['customer_name'],
                    'customer_email': row['customer_email'],
                    'created_at': row['created_at'],
                    'items': row['items'] or 'No items'
                }
                for row in cursor.fetchall()
            ]
        
        return _build_success_response({'orders': orders})
    except Exception as error:
        return _build_error_response(str(error), 500)


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def handle_get_order_details(order_id: int) -> Tuple[Dict[str, Any], int]:
    """
    Get detailed information about a specific order.
    
    Args:
        order_id: The order identifier.
        
    Returns:
        JSON response with order details including items and total.
    """
    try:
        order_header_query = """
            SELECT o.id, o.customer_id, o.created_at, 
                   c.name AS customer_name, c.email AS customer_email
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            WHERE o.id = ?
        """
        
        order_items_query = """
            SELECT oi.isbn, b.title, b.author, b.price, oi.qty, 
                   (b.price * oi.qty) AS line_total
            FROM order_items oi
            JOIN books b ON oi.isbn = b.isbn
            WHERE oi.order_id = ?
        """
        
        with closing(get_connection()) as connection:
            # Get order header
            cursor = connection.execute(order_header_query, (order_id,))
            order = cursor.fetchone()
            
            if not order:
                return _build_error_response('Order not found', 404)
            
            # Get order items
            cursor = connection.execute(order_items_query, (order_id,))
            items = [dict(row) for row in cursor.fetchall()]
            
            total = sum(item['line_total'] for item in items)
            
            return _build_success_response({
                'order_id': order['id'],
                'customer_id': order['customer_id'],
                'customer_name': order['customer_name'],
                'customer_email': order['customer_email'],
                'created_at': order['created_at'],
                'items': items,
                'total': round(total, 2)
            })
    except Exception as error:
        return _build_error_response(str(error), 500)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', DEFAULT_PORT))
    app.run(host=DEFAULT_HOST, port=port, debug=True)
