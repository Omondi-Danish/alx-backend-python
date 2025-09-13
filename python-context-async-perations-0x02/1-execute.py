import sqlite3

class ExecuteQuery:
    """
    A reusable context manager that:
    - Opens a database connection
    - Executes a given query with optional parameters
    - Returns the results inside the with block
    """
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.results = None

    def __enter__(self):
        # Step 1: Open the database connection
        self.conn = sqlite3.connect(self.db_name)
        print(f"[INFO] Connected to database: {self.db_name}")

        # Step 2: Execute the query
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()

        # Step 3: Return results directly, so user gets data in 'as' variable
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Step 4: Always close the connection
        if self.conn:
            self.conn.close()
            print(f"[INFO] Database connection closed.")

        if exc_type:
            print(f"[ERROR] Exception occurred: {exc_val}")

        # Return False so exceptions are not suppressed
        return False


# --- Using the Context Manager ---
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery('users.db', query, params) as results:
    print("[RESULTS]", results)
