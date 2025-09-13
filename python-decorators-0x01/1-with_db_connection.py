import sqlite3
import functools

def with_db_connection(func):
    """Decorator that opens a database connection, passes it to the function, and closes it afterward"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Step 1: Open connection
        conn = sqlite3.connect('users.db')
        try:
            # Step 2: Call the original function, but pass the connection as first argument
            return func(conn, *args, **kwargs)
        finally:
            # Step 3: Close connection no matter what (even if an error happens)
            conn.close()

    return wrapper


# Step 4: Use the decorator
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Step 5: Test the function
user = get_user_by_id(user_id=1)
print(user)
