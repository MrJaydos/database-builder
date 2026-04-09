import sqlite3

conn = sqlite3.connect('names.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM names WHERE origin IS NOT NULL LIMIT 5000")
for row in cursor.fetchall():
    print(row)