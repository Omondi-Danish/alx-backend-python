import sqlite3
import functools

# Step 1: Copy the with_db_connection decorator from previous task
def with_db_connection(func):
    """Decorator that opens a database connection, passes it to the function, and closes it afterward"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


# Step 2: Create the transactional decorator
def transactional(func):
    """Decorator that wraps a function call in a database transaction"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # Run the function
            conn.commit()  # ✅ Commit changes if successful
            return result
        except Exception as e:
            conn.rollback()  # ❌ Rollback if something went wrong
            print(f"[ERROR] Transaction rolled back due to: {e}")
            raise  # Re-raise the error so we know something failed
    return wrapper


# Step 3: Use both decorators
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Step 4: Test the function
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
print("✅ Email updated successfully")
