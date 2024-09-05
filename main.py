import ollama, sqlite3, sys

if len(sys.argv) < 2:
    print("Missing argument: SQLite database path\neg: python main.py path/to/database.db")
    exit(1)

database = sys.argv[1]
contents = []

def get_tables(database):
    with sqlite3.connect(database) as conn:
        with conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            return tables

def get_data(database, table):
    with sqlite3.connect(database) as conn:
        with conn:
            cursor = conn.execute("SELECT * FROM " + table[0] + ";")
            data = cursor.fetchall()
            return data

def get_schema(database, table):
    with sqlite3.connect(database) as conn:
        with conn:
            cursor = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='" + table[0] + "';")
            schema = cursor.fetchall()
            return schema

def prompt_ai(prompt, contents):
    return ollama.generate(
        model='llama3.1',
        prompt= f"contents: {contents}, prompt: {prompt}",
        raw= True
    )

try:
    tables = get_tables(database)
    for table in tables:
        schema = get_schema(database, table)
        data = get_data(database, table)
        contents.append({"schema": schema, "data": data})

    prompt = input("Enter your prompt: ")
    response = prompt_ai(prompt, contents)
    print(response["response"])
          
except sqlite3.OperationalError:
        print("Invalid database path")
        exit(1)