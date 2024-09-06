import ollama, sqlite3, sys, os, time
os.system('cls' if os.name == 'nt' else 'clear')

if len(sys.argv) < 2:
    print("Missing argument: SQLite database path\neg: python main.py path/to/database.db")
    exit(1)

database = sys.argv[1]
contents = []

messages = []

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

def prompt_ai(prompt, contents, messages):
    messages.append({"role": "user", "content": f"prompt: {prompt}\ncontent: {contents}"})

    duration = time.time()
    print("----\nRESPONSE:")

    response = ollama.chat(
        model='llama3.1',
        messages= messages,
        stream= True
    )

    full_response = ""
    for chunk in response:
        content = chunk['message']['content']
        print(content, end='', flush=True)
        full_response += content

    return full_response


if __name__ == "__main__":
    try:
        tables = get_tables(database)
        print(f"Loading database: {database}")

        messages= [
            {"role": "system", "content": """
You are an assistant that responds to user inquiries regarding their own SQLite3 databases.
You are given a prompt, and content - which contains the schema and data of the database.
Do not hallucinate. Keep it natural, concise, and relevant to the prompt. Do not explain unless asked to, have a conversation with the user.
Do not include any code.
Your output must only be plain text, no markdown or rich text formatting - no bolding or italic, unless the user specified you to.
            """},
        ]

        num = 0
        for table in tables:
            num += 1

            schema = get_schema(database, table)
            data = get_data(database, table)
            contents.append({"schema": schema, "data": data})

            print(f"{num}/{len(tables)} Loaded table '{table[0]}'")

        summary = prompt_ai(f"Hello! Suggest what actions can be done with the database {database}, start by asking the user what the database is about", contents, messages)
        while True:
            prompt = input("\n---------\nPROMPT: ")
            if prompt == "exit":
                exit()
            else:
                response = prompt_ai(prompt, contents, messages)

    except sqlite3.OperationalError:
            print("Invalid database path")
            exit(1)