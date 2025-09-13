import sqlite3
import functools

# Step 1: Create a simple dictionary to store cached results
query_cache = {}

# Step 2: Copy our with_db_connection decorator from previous tasks
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


# Step 3: Implement the cache_query decorator
def cache_query(func):
    """
    Decorator that caches results based on the SQL query string.
    If the same query is called again, it returns the cached result instead of hitting the database.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Assume query is passed as a keyword argument
        query = kwargs.get("query")
        if query in query_cache:
            print(f"[CACHE] Using cached result for query: {query}")
            return query_cache[query]

        # If not cached, execute function and store result
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print(f"[CACHE] Stored result for query: {query}")
        return result

    return wrapper


# Step 4: Use the decorators
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Step 5: Test caching
# First call will hit the database and store the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached data
users_again = fetch_users_with_cache(query="SELECT * FROM users")
