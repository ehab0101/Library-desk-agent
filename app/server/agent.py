import traceback
from typing import Dict, List, Any, Optional, Tuple
import google.genai as genai
from google.genai import types

from tools import (
    find_books,
    create_order,
    restock_book,
    update_price,
    order_status,
    inventory_summary
)
from models import save_tool_call
from tool_declarations import get_all_tool_declarations
from config import (
    GOOGLE_API_KEY,
    GEMINI_MODEL_NAME,
    LLM_TEMPERATURE,
    SYSTEM_INSTRUCTION,
    MAX_TOOL_ITERATIONS,
    DEFAULT_SESSION_ID
)


_client = genai.Client(api_key=GOOGLE_API_KEY)

_TOOL_MAP: Dict[str, Any] = {
    "find_books": find_books,
    "create_order": create_order,
    "restock_book": restock_book,
    "update_price": update_price,
    "order_status": order_status,
    "inventory_summary": inventory_summary
}

_chat_sessions: Dict[str, Any] = {}


def _create_chat_session() -> Any:
    tool_declarations = get_all_tool_declarations()
    library_tool = types.Tool(function_declarations=tool_declarations)
    
    return _client.chats.create(
        model=GEMINI_MODEL_NAME,
        config=types.GenerateContentConfig(
            tools=[library_tool],
            temperature=LLM_TEMPERATURE,
            system_instruction=SYSTEM_INSTRUCTION
        )
    )


def _get_or_create_chat_session(session_id: str) -> Any:
    if session_id not in _chat_sessions:
        _chat_sessions[session_id] = _create_chat_session()
    return _chat_sessions[session_id]


def _extract_tool_calls_and_text(parts: List[Any]) -> Tuple[List[Any], List[str]]:
    tool_calls = []
    text_parts = []
    
    for part in parts:
        if hasattr(part, "function_call") and part.function_call:
            tool_calls.append(part.function_call)
        elif hasattr(part, "text") and part.text:
            text_parts.append(part.text)
    
    return tool_calls, text_parts


def _format_tool_result(result: Any) -> Dict[str, Any]:
    if isinstance(result, list):
        return {"items": result, "count": len(result)}
    if isinstance(result, dict):
        return result
    return {"result": str(result)}


def _execute_tool(
    tool_name: str,
    arguments: Dict[str, Any],
    session_id: str
) -> types.Part:
    if tool_name not in _TOOL_MAP:
        return types.Part(
            function_response=types.FunctionResponse(
                name=tool_name,
                response={"error": f"Unknown tool: {tool_name}"}
            )
        )
    
    try:
        tool_function = _TOOL_MAP[tool_name]
        result = tool_function.invoke(arguments)
        
        try:
            result_for_logging = result if isinstance(result, dict) else {"result": result}
            save_tool_call(session_id, tool_name, arguments, result_for_logging)
        except Exception as save_error:
            print(f"Warning: Failed to save tool call: {save_error}")
        
        formatted_result = _format_tool_result(result)
        
        return types.Part(
            function_response=types.FunctionResponse(
                name=tool_name,
                response=formatted_result
            )
        )
    
    except Exception as error:
        error_message = f"{str(error)}\n{traceback.format_exc()}"
        
        try:
            save_tool_call(session_id, tool_name, arguments, {"error": str(error)})
        except Exception:
            pass
        
        return types.Part(
            function_response=types.FunctionResponse(
                name=tool_name,
                response={"error": error_message}
            )
        )


def _extract_final_text(response: Any) -> str:
    candidate = response.candidates[0]
    parts = candidate.content.parts
    text_parts = []
    
    for part in parts:
        if hasattr(part, "text") and part.text:
            text_parts.append(part.text)
    
    return "\n".join(text_parts).strip() if text_parts else "No response generated."


def library_agent(
    user_message: str,
    session_id: str = DEFAULT_SESSION_ID,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> str:
    try:
        chat = _get_or_create_chat_session(session_id)
        
        response = chat.send_message(user_message)
        
        iteration = 0
        while iteration < MAX_TOOL_ITERATIONS:
            iteration += 1
            candidate = response.candidates[0]
            parts = candidate.content.parts
            
            tool_calls, text_parts = _extract_tool_calls_and_text(parts)
            
            if text_parts and not tool_calls:
                return "\n".join(text_parts).strip()
            
            if tool_calls:
                function_responses = [
                    _execute_tool(
                        tool_call.name,
                        tool_call.args or {},
                        session_id
                    )
                    for tool_call in tool_calls
                ]
                
                response = chat.send_message(function_responses)
            else:
                if text_parts:
                    return "\n".join(text_parts).strip()
                break
        
        return _extract_final_text(response)
    
    except Exception as error:
        error_trace = traceback.format_exc()
        return f"Agent Error: {str(error)}\n{error_trace}"


if __name__ == "__main__":
    test_queries = [
        "Do you have Clean Code?",
        "We sold 3 copies of Clean Code to customer 2 today. Create the order.",
        "Restock The Pragmatic Programmer by 10 copies.",
        "Update the price of Effective Modern C++ to 45.",
        "What's the status of order 3?",
        "Show me all low-stock books"
    ]
    
    print("--- Library Agent Test ---")
    for query in test_queries:
        print(f"\n> User: {query}")
        print(f"Agent: {library_agent(query)}")
