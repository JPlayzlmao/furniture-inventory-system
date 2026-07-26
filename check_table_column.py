import sqlite3

connection = sqlite3.connect("inventory.db")
cursor = connection.cursor()

cursor.execute("""SELECT * FROM orders""")

for column in cursor.description:
    print(column[0])

connection.close()