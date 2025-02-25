import sqlite3

conn = sqlite3.connect("comedor.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS mesas (id INTEGER PRIMARY KEY, estado TEXT)")
for i in range(1, 11):
    cursor.execute("INSERT INTO mesas (id, numero, estado) VALUES (?, ?, ?) ON CONFLICT(id) DO NOTHING", (i, i, "Libre"))

conn.commit()
conn.close()