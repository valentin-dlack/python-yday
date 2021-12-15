from faker import Faker
import pandas as pd
from random import randint, randrange
import sqlite3

conn = sqlite3.connect("faker.db")
cursor = conn.cursor()

fake = Faker("fr-FR")

def select(query):
    res = []
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        res.append(row)
    return res

def insert(query, values):
    cursor.execute(query, values)
    conn.commit()

def createUpdateDelete(query):
    cursor.execute(query)
    conn.commit()

def fill(nbr): #nbr -> nombre de lignes a remplir
    for i in range(nbr):
        guildId = randint(10000000000000000, 99999999999999999)
        userId = randint(10000000000000000, 99999999999999999)
        insert("INSERT INTO guilds (id, totalXp) VALUES (?, ?)", (guildId, 0))
        #generate id for random guild ID
        gRows = select("SELECT * FROM guilds")
        g_Id = gRows[randint(0, len(gRows)-1)][0]
        insert("INSERT INTO users (id, username, xpAmount, xpLevel, guildId) VALUES (?,?,?,?,?)",
        (userId, fake.user_name(), fake.random_int(), randint(0, 100), g_Id))

        #update totalxp amount on guild table
        totalRow = select("""SELECT guilds.id, sum(users.xpAmount) AS totalXp FROM guilds
        INNER JOIN users ON users.guildId = guilds.id
        GROUP BY guilds.id
        ORDER BY totalXp;""")
        for guild in totalRow:
            insert("UPDATE guilds SET totalXp = (?) WHERE id = (?)", (guild[1], guild[0]))

def export(query):
    sql_query = pd.read_sql_query(query, conn)
    df = pd.DataFrame(sql_query)
    df.to_excel('./exported.xlsx', index=False)

export("SELECT * FROM users")

conn.close()