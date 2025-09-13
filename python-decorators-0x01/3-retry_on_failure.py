import time
import sqlite3
import functools

# Step 1: Copy the with_db_connection decorator from previous tasks
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


# Step 2: Create the retry_on_failure decorator
def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries the function call if it raises an exception.
    :param retries: Number of times to retry before giving up
    :param delay: Seconds to wait between retries
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)  # Try to execute function
                except Exception as e:
                    attempt += 1
                    print(f"[WARNING] Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("[ERROR] All retry attempts failed.")
                        raise  # re-raise last exception
        return wrapper
    return decorator


# Step 3: Use the decorators
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Step 4: Test the function
users = fetch_users_with_retry()
print(users)
