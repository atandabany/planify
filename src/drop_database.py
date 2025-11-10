import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor = db.cursor()

cursor.execute("DROP DATABASE IF EXISTS planify")
print("Base supprimée")

cursor.close()
db.close()
