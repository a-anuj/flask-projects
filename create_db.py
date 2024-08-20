import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="anuj2006"
)
my_cursor = mydb.cursor()
my_cursor.execute("USE list_users;")
#my_cursor.execute("CREATE DATABASE list_users")
#my_cursor.execute("SHOW DATABASES")
my_cursor.execute("ALTER TABLE users ADD COLUMN password_hash VARCHAR(128);")
for db in my_cursor:
    print(db)
