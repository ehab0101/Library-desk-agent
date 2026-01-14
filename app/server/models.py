import json
from typing import List, Dict, Any, Optional
from contextlib import closing
from db import get_connection


def save_message(session_id: str, role: str, content: str) -> None:
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
    with closing(get_connection()) as connection:
        connection.execute(
            "INSERT INTO tool_calls (session_id, name, args_json, result_json) VALUES (?, ?, ?, ?)",
            (session_id, tool_name, json.dumps(arguments), json.dumps(result))
        )
        connection.commit()


def get_session_messages(session_id: str) -> List[Dict[str, Any]]:
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
    query = "SELECT DISTINCT session_id FROM messages ORDER BY session_id"
    
    with closing(get_connection()) as connection:
        cursor = connection.execute(query)
        return [row['session_id'] for row in cursor.fetchall()]


def get_tool_calls(session_id: Optional[str] = None) -> List[Dict[str, Any]]:
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
