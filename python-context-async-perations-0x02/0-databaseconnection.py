import sqlite3

class DatabaseConnection:
    """
    A custom context manager to handle opening and closing database connections.
    Implements __enter__ and __exit__ so we can use it with the 'with' statement.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # This is called when entering the 'with' block
        self.conn = sqlite3.connect(self.db_name)
        print(f"[INFO] Connected to database: {self.db_name}")
        return self.conn  # this value will be assigned to the variable after 'as'

    def __exit__(self, exc_type, exc_val, exc_tb):
        # This is called when exiting the 'with' block
        if self.conn:
            self.conn.close()
            print(f"[INFO] Database connection closed.")

        # If an exception occurred inside the with block, we could handle it here
        if exc_type:
            print(f"[ERROR] An error occurred: {exc_val}")
        # Returning False means any exception will still propagate
        return False


# --- Using the Context Manager ---
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("[RESULTS]", results)
