import signal
import sys
import time
import threading
import psycopg2

con = psycopg2.connect(
    database="flink",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = con.cursor()
name = "Vasia1"
full_name = "SMITH2"
cur.execute(
    "INSERT INTO users (name,full_name,greeting) VALUES ('%s', '%s', 'Nice to see you at the 445-nth time George Vasilev!')" % (name, full_name)
)

con.commit()
print("Record inserted successfully")
con.close()