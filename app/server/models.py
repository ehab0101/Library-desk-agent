"""
Database models for chat message and tool call storage.

This module provides functions for persisting and retrieving
chat messages and tool execution logs.
"""
import json
from typing import List, Dict, Any, Optional
from contextlib import closing
from db import get_connection


def save_message(session_id: str, role: str, content: str) -> None:
    """
    Save a chat message to the database.
    
    Args:
        session_id: Unique identifier for the chat session.
        role: Message role - 'user' or 'assistant'.
        content: The message content text.
    """
    with closing(get_connection()) as connection:
        connection.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content)
        )
        connection.commit()


def save_tool_call(
    session_id: str,
    tool_name: str,
    arguments: Dict[str, Any],
    result: Dict[str, Any]
) -> None:
    """
    Save a tool execution log to the database.
    
    Args:
        session_id: The session ID where the tool was called.
        tool_name: Name of the tool that was executed.
        arguments: Dictionary of arguments passed to the tool.
        result: Dictionary containing the tool execution result.
    """
    with closing(get_connection()) as connection:
        connection.execute(
            "INSERT INTO tool_calls (session_id, name, args_json, result_json) VALUES (?, ?, ?, ?)",
            (session_id, tool_name, json.dumps(arguments), json.dumps(result))
        )
        connection.commit()


def get_session_messages(session_id: str) -> List[Dict[str, Any]]:
    """
    Retrieve all messages for a specific session.
    
    Args:
        session_id: The session identifier.
        
    Returns:
        List[Dict[str, Any]]: List of message dictionaries ordered by creation time.
    """
    query = """
        SELECT id, role, content, created_at 
        FROM messages 
        WHERE session_id = ? 
        ORDER BY created_at ASC
    """
    
    with closing(get_connection()) as connection:
        cursor = connection.execute(query, (session_id,))
        return [dict(row) for row in cursor.fetchall()]


def get_sessions() -> List[str]:
    """
    Retrieve a list of all unique session IDs.
    
    Returns:
        List[str]: List of session ID strings, ordered alphabetically.
    """
    query = "SELECT DISTINCT session_id FROM messages ORDER BY session_id"
    
    with closing(get_connection()) as connection:
        cursor = connection.execute(query)
        return [row['session_id'] for row in cursor.fetchall()]


def get_tool_calls(session_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieve tool call logs, optionally filtered by session.
    
    Args:
        session_id: Optional session ID to filter by. If None, returns all tool calls.
        
    Returns:
        List[Dict[str, Any]]: List of tool call dictionaries ordered by creation time.
    """
    if session_id:
        query = """
            SELECT id, session_id, name, args_json, result_json, created_at 
            FROM tool_calls 
            WHERE session_id = ? 
            ORDER BY created_at ASC
        """
        params = (session_id,)
    else:
        query = """
            SELECT id, session_id, name, args_json, result_json, created_at 
            FROM tool_calls 
            ORDER BY created_at ASC
        """
        params = ()
    
    with closing(get_connection()) as connection:
        cursor = connection.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
