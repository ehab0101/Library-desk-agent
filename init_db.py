import sqlite3
import os

DB_DIR = os.path.join(os.path.dirname(__file__), 'app', 'db')
DB_PATH = os.path.join(DB_DIR, 'library.db')
SCHEMA_PATH = os.path.join(DB_DIR, 'schema.sql')
SEED_PATH = os.path.join(DB_DIR, 'seed.sql')

def init_database():
    os.makedirs(DB_DIR, exist_ok=True)
    
    if os.path.exists(DB_PATH):
        print(f"Removing existing database at {DB_PATH}")
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Creating database schema...")
    
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    
    print("Seeding database...")
    
    with open(SEED_PATH, 'r') as f:
        seed_sql = f.read()
        cursor.executescript(seed_sql)
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized successfully at {DB_PATH}")
    print("\nSeed data:")
    print("- 10 books")
    print("- 6 customers")
    print("- 4 orders")
    print("\nYou can now start the server with: python app/server/main.py")

if __name__ == '__main__':
    init_database()
