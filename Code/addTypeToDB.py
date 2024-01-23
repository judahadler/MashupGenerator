# import required module
import os
from os import listdir
from os.path import isfile, join
import mariadb
import sys

##start Connect to MariaDB Platform ##
try:
    conn = mariadb.connect(
        user="elliottadler",
        password="",
        host="localhost",
        port=3306,
        database="test",
        autocommit=True

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

cur.execute("SELECT * FROM instrumentals")

    # Print Result-set
for (r) in cur:
    cur.execute("INSERT INTO instrumentals (type) VALUES (?)", 
        ("Instrumental"))