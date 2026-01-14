# Library Desk Agent

A local chat interface for a Library Desk Agent that can answer questions and perform actions via tools that read/write a SQLite database.

## Project Overview

This project implements an AI-powered Library Desk Agent using Google Gemini with function calling capabilities. The agent can interact with a SQLite database to manage books, customers, and orders through natural language conversations.

## Features

- **AI-Powered Chat**: Google Gemini LLM with function calling
- **Interactive UI**: Modern chat interface with dark/light mode
- **Database Operations**: Full CRUD operations via tools
- **Session Management**: Multiple conversation sessions
- **6 Tools**: Complete library management functionality

## Project Structure

```
library-desk-agent/
├── app/
│   ├── frontend/              # Frontend UI
│   │   ├── index.html         # Main chat interface
│   │   └── app.js             # Frontend logic
│   ├── server/                # Backend server
│   │   ├── main.py            # Flask REST API
│   │   ├── agent.py           # AI agent orchestration
│   │   ├── tools.py           # Langchain tools (6 tools)
│   │   ├── db.py              # Database utilities
│   │   ├── models.py          # Data access layer
│   │   ├── config.py          # Configuration constants
│   │   └── tool_declarations.py # Tool schemas
│   ├── db/                    # Database files
│   │   ├── schema.sql         # Database schema
│   │   ├── seed.sql           # Seed data (10 books, 6 customers, 4 orders)
│   │   └── library.db        # SQLite database (auto-generated)
│   └── prompts/               # Prompts
│       └── system_prompt.txt  # System instruction
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── init_db.py                 # Database initialization script
├── start.bat                  # Windows start script
├── start.sh                   # Linux/Mac start script
└── README.md                  # This file
```

## Quick Start

### Option 1: Easy Start (Recommended)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

3. **Initialize Database**
   ```bash
   python init_db.py
   ```

4. **Start Server**
   ```bash
   cd app/server
   python main.py
   ```

5. **Open Frontend**
   - Open `app/frontend/index.html` in your browser
   - Or serve with: `cd app/frontend && python -m http.server 8000`

## 📋 Requirements

### Required Files (All Present)

#### `/app/frontend/`
- ✅ `index.html` - Chat UI with dark/light mode
- ✅ `app.js` - Frontend JavaScript

#### `/app/server/`
- ✅ `main.py` - Flask REST API endpoints
- ✅ `agent.py` - LLM agent with tool integration
- ✅ `tools.py` - 6 Langchain tools
- ✅ `db.py` - Database connection utilities
- ✅ `models.py` - Chat storage models
- ✅ `config.py` - Configuration constants
- ✅ `tool_declarations.py` - Tool schema definitions

#### `/app/db/`
- ✅ `schema.sql` - Database schema (all tables)
- ✅ `seed.sql` - Seed data (10 books, 6 customers, 4 orders)

#### `/app/prompts/`
- ✅ `system_prompt.txt` - System instruction for agent

#### Root Files
- ✅ `.env.example` - Environment variables template
- ✅ `README.md` - Complete documentation
- ✅ `requirements.txt` - Python dependencies
- ✅ `init_db.py` - Database initialization script
- ✅ `start.bat` / `start.sh` - Run scripts

## 🛠️ Tools Implemented

1. **`find_books({q, by})`** - Search books by title or author
2. **`create_order({customer_id, items})`** - Create order and reduce stock
3. **`restock_book({isbn, qty})`** - Increase book stock
4. **`update_price({isbn, price})`** - Update book price
5. **`order_status({order_id})`** - Get order details
6. **`inventory_summary()`** - List low-stock books

## Database Schema

### Domain Tables
- `books` - ISBN (PK), title, author, price, stock
- `customers` - id (PK), name, email
- `orders` - id (PK), customer_id (FK), created_at
- `order_items` - order_id (FK), isbn (FK), qty

### Chat Storage
- `messages` - id, session_id, role, content, created_at
- `tool_calls` - id, session_id, name, args_json, result_json, created_at

## Seed Data

- **10 Books**: Programming and software engineering books
- **6 Customers**: Sample customer records
- **4 Orders**: Sample order history

## Configuration

### Environment Variables

Create `.env` from `.env.example`:

```env
GOOGLE_API_KEY=your_api_key_here
PORT=5000
```

Get API key from: https://makersuite.google.com/app/apikey

## 📡 API Endpoints

- `POST /api/chat` - Send chat message
- `GET /api/sessions` - List all sessions
- `GET /api/sessions/<id>/messages` - Get session messages
- `GET /api/orders` - List all orders
- `GET /api/orders/<id>` - Get order details
- `GET /api/health` - Health check

## UI Features

- **Dark/Light Mode**: Toggle with moon/sun icon
- **Session Management**: Create and switch between sessions
- **Responsive Design**: Works on desktop and mobile
- **Real-time Chat**: Instant responses

## Sample Scenarios

### Scenario 1: Create Order
```
User: "We sold 3 copies of Clean Code to customer 2 today. Create the order and adjust stock."
Agent: [Calls find_books, then create_order, responds with order ID and new stock]
```

### Scenario 2: Restock and Search
```
User: "Restock The Pragmatic Programmer by 10 and list all books by Andrew Hunt."
Agent: [Calls restock_book, then find_books, responds with results]
```

### Scenario 3: Check Order Status
```
User: "What's the status of order 3?"
Agent: [Calls order_status, responds with order details]
```

## Testing

### Test Agent
```bash
cd app/server
python agent.py
```

### Test Tools
```bash
cd app/server
python -c "from tools import find_books; print(find_books.invoke({'q': 'Clean', 'by': 'title'}))"
```

### Test Database
```bash
python -c "from app.server.db import get_all_books; print(get_all_books())"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Database not found | Run `python init_db.py` |
| Module not found | Run `pip install -r requirements.txt` |
| Port already in use | Change PORT in `.env` or `config.py` |
| API key error | Check `.env` file has correct `GOOGLE_API_KEY` |
| CORS errors | Ensure `flask-cors` is installed |

## Code Quality

- ✅ Clean code principles applied
- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ Separation of concerns
- ✅ Error handling
- ✅ Constants extraction

## Security Notes

- API key stored in environment variables
- SQL injection prevention (parameterized queries)
- Input validation in tools
- No authentication (as per requirements)

## License

This project is for educational purposes.

## Credits

Built with:
- Google Gemini API
- Langchain
- Flask
- SQLite

---

**Ready to use!** Just run `start.bat` (Windows) or `./start.sh` (Linux/Mac) and open the frontend!
