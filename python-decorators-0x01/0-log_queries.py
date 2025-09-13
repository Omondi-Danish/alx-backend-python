import sqlite3
import functools

# Step 1: Create the decorator
def log_queries(func):
    """Decorator that logs SQL queries before running them"""

    @functools.wraps(func)  # This keeps the original function's name and docstring
    def wrapper(*args, **kwargs):
        # Check if the query is passed as a positional or keyword argument
        query = kwargs.get("query") if "query" in kwargs else args[0] if args else None
        
        if query:
            print(f"[LOG] Executing SQL Query: {query}")  # Log the query before running

        return func(*args, **kwargs)  # Call the original function

    return wrapper


# Step 2: Use the decorator
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Step 3: Test the function
users = fetch_all_users(query="SELECT * FROM users")
print(users)
