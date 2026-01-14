"""
Configuration constants for the Library Desk Agent application.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyAhuxqmnAfYV5dudm2qUCQK5omjF54P0d8')
GEMINI_MODEL_NAME = "gemini-2.0-flash"
LLM_TEMPERATURE = 0.0

# Database Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATABASE_PATH = PROJECT_ROOT / "app" / "db" / "library.db"

# Agent Configuration
MAX_TOOL_ITERATIONS = 5
CONVERSATION_HISTORY_LIMIT = 10
DEFAULT_SESSION_ID = "default"

# Tool Configuration
LOW_STOCK_THRESHOLD = 5
VALID_SEARCH_FIELDS = ("title", "author")

# Server Configuration
DEFAULT_PORT = 5000
DEFAULT_HOST = "0.0.0.0"

# System Instructions
SYSTEM_INSTRUCTION = (
    "You are a helpful library assistant. Always use tools for DB actions "
    "like searching books, creating orders, restocking, updating prices, "
    "checking inventory, and order status. When you use tools, explain the results "
    "clearly to the user in natural language. Remember previous conversations in this session."
)
