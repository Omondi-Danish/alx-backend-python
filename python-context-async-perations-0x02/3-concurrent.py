import asyncio
import aiosqlite

# Step 1: Define async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("[INFO] All Users:", results)
            return results

# Step 2: Define async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("[INFO] Users older than 40:", results)
            return results

# Step 3: Function that runs both concurrently using asyncio.gather
async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

# Step 4: Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
