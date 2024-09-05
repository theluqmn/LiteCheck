import ollama, sqlite3, sys

if len(sys.argv) < 2:
    print("Missing argument: SQLite database path\neg: python main.py path/to/database.db")
    exit(1)

database = sys.argv[1]
try:
    with sqlite3.connect(database) as conn:
        with conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print("Tables in the database:")
            for table in tables:
                print(table[0])
except sqlite3.OperationalError:
        print("Invalid database path")
        exit(1)