import sqlite3

conn = sqlite3.connect("battleship_scores.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM scores")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()