import mysql.connector
from mysql.connector import errorcode
from datetime import date

# retrieve matrix from database into

conn = mysql.connector.connect(
        user="root",
        host="localhost",
        database="testdb"
    )



aa = -1
bb = -2
cc = -3



matrix =[]

def retrieve_matrix(conn):

    print("read")
    cursor = conn.cursor()
    cursor.execute("select * from goose")
    records = cursor.fetchall()
    for row in records:
        matrix.append(row)
    #print("retieved matrix",matrix)


def add_submatrix(conn):
    print("Create")

    cursor = conn.cursor()
    sql = "INSERT INTO goose (a,b,c) VALUES (%s, %s, %s)"
    val = (store_action[0], store_action[1],store_action[2])
    cursor.execute(sql, val)

    conn.commit()


def delete_submatrix(conn):
    print("Delete")
    cursor = conn.cursor()
    cursor.execute(
        'delete from goose LIMIT 1'
    )
    conn.commit()
store_action = [-6,-6,-6]

# morning 4:30

retrieve_matrix(conn)
print(matrix)

delete_submatrix(conn)
retrieve_matrix(conn)
print(matrix)

add_submatrix(conn)
retrieve_matrix(conn)
print(matrix)