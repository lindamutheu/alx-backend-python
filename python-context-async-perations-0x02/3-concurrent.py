import asyncio
import aiosqlite

# ✅ Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
        print("[ALL USERS]", results)
        return results

# ✅ Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        results = await cursor.fetchall()
        await cursor.close()
        print("[USERS > 40]", results)
        return results

# ✅ Run both queries concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# ✅ Run the concurrent queries
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
