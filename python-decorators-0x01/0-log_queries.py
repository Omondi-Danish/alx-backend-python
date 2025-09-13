import sqlite3
import functools
from datetime import datetime  # ✅ Added as required

# Step 1: Create the log_queries decorator
def log_queries(func):
    """
    Decorator that logs the SQL query before executing it.
    It also prints a timestamp when the query is logged.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", None)
        if query:
            print(f"[{datetime.now()}] Executing query: {query}")
        else:
            print(f"[{datetime.now()}] Executing function without query argument.")
        return func(*args, **kwargs)
    return wrapper


# Step 2: Apply decorator to function
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Step 3: Run the function to test
users = fetch_all_users(query="SELECT * FROM users")
print(users)
