# import pyodbc
import matplotlib.pyplot as plt
from datetime import datetime
import mysql.connector

conn = mysql.connector.connect(
        user="root",
        host="localhost",
        database="golden"
    )


def read_overall(conn):
    date_from_str = "11/04/22"
    date_from = datetime.strptime(date_from_str, '%d/%m/%y')
    date_to_str = "11/04/22"
    date_to = datetime.strptime(date_to_str, '%d/%m/%y')
    overall_results = 0
    cursor = conn.cursor()
    sql = "select sum(Results) from reports_b_noon where Date BETWEEN %s AND %s"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        overall_results = row[0]
    overall = overall_results
    return overall

# Overall results

overall = read_overall(conn)
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
x = ["Overall Results"]
ax.bar(x, overall)
plt.text(0, overall, str(overall))
plt.show()