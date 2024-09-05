import ollama, sqlite3, sys, os
os.system('cls' if os.name == 'nt' else 'clear')

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
    response = ollama.generate(
        model='llama3.1',
        prompt= f"contents: {contents}, prompt: {prompt}",
        raw= True
    )
    return response["response"]


if __name__ == "__main__":
    try:
        tables = get_tables(database)
        print(f"Loading database: {database}")

        num = 0
        for table in tables:
            num += 1

            schema = get_schema(database, table)
            data = get_data(database, table)
            contents.append({"schema": schema, "data": data})

            print(f"{num}/{len(tables)} Loaded table '{table[0]}'")

        print("It may take a while to generate the response, please be patient")
        print(prompt_ai(f"Give a simple overview of what the database does, the path is {database}", contents))
            
    except sqlite3.OperationalError:
            print("Invalid database path")
            exit(1)