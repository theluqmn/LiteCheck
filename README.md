# LiteCheck

Get insights on your SQLite databases, powered by Ollama, llama 3.1 8b

----
Make inquiries on your SQLite database using Llama 3.1 locally, with no internet connection required. A fun project for me to complete in a single night.

## How to run

### Prerequisites

- You need to have Ollama installed in your device, and the Llama 3.1 8b model.
- Python 3.12 or higher (this project was written with Python 3.12.4)

### Getting started

1. Clone the repository
2. Run the Python file, with the directory of your SQLite3 database
   `python main.py C:\Users\test\Documents\Code\test\database.db`
3. Give some moments for the code to process your database, then you should be able to chat with the model.

## To-do

- [x] Read all tables in database
- [ ] Link database to Ollama
- [ ] Chat with Ollama
- [ ] Model run SQL commands according to prompts
As of now, I have no plans to support other SQL-based databases.

I have an idea to create an interactive, web-based version that still runs locally using Ollama. Just an idea, not gonna work on it at the moment.
