import sqlite3

# ✅ Class-based context manager for executing a query
class ExecuteQuery:
    def __init__(self, db_file, query, params=()):
        self.db_file = db_file
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("[INFO] Connection closed.")

# ✅ Use the context manager
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery('users.db', query, params) as results:
    print("[RESULTS]", results)
