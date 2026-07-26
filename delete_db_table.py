import sqlite3

connection = sqlite3.connect("inventory.db")
cursor = connection.cursor()
                                    #table[-v-]
cursor.execute("DROP TABLE IF EXISTS order_items")

connection.commit()
connection.close()

print("table deleted.")