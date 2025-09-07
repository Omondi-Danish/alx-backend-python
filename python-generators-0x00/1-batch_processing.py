import mysql.connector

def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:  # yield remaining rows
            yield batch

        cursor.close()
        connection.close()
        return  # ✅ Added return for completeness

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return  # ✅ Added return in error case

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
    return  # ✅ Added return for completeness
