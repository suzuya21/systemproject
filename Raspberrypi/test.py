"""
mysql接続テスト
"""
import mysql.connector as mydb
import time

# コネクションの作成
conn = mydb.connect(
    host='localhost',
    port='3306',
    user='root',
    password='root',
    database='sousei_db'
)
cur = conn.cursor()
start = time.time()
cur.execute("select * from syusseki")
a = cur.fetchall()
print(time.time()-start)
#print(a)
