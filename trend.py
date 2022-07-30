import matplotlib.pyplot as plt
from datetime import datetime
import mysql.connector
import plotly.graph_objects as go

conn = mysql.connector.connect(
        user="root",
        host="localhost",
        database="golden"
    )

date_from_str = "19/07/22"
date_from = datetime.strptime(date_from_str, '%d/%m/%y')
date_to_str = "22/07/22"
date_to = datetime.strptime(date_to_str, '%d/%m/%y')


def read_reports(conn):
    result1 = []
    date1 = []
    cursor = conn.cursor()

    sql = "select sum(Results) from reports where Date BETWEEN %s AND %s GROUP by Date"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        result1.append(row)

    sql = "select Date from reports where Date BETWEEN %s AND %s GROUP by Date"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        date1.append(row)

    return result1, date1

def read_b(conn):
    result2 = []
    date2 = []
    cursor = conn.cursor()

    sql = "select sum(Results) from reports_b where Date BETWEEN %s AND %s GROUP by Date"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        result2.append(row)

    sql = "select Date from reports_b where Date BETWEEN %s AND %s GROUP by Date"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        date2.append(row)

    return result2, date2


def read_noon(conn):
    result3 = []
    date3 = []
    cursor = conn.cursor()

    sql = "select sum(Results) from reports_noon where Date BETWEEN %s AND %s GROUP by Date"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        result3.append(row)

    sql = "select Date from reports_noon where Date BETWEEN %s AND %s GROUP by Date"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        date3.append(row)

    return result3, date3


def read_b_noob(conn):
    result4 = []
    date4 = []
    cursor = conn.cursor()

    sql = "select sum(Results) from reports_b_noon where Date BETWEEN %s AND %s GROUP by Date"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        result4.append(row)

    sql = "select Date from reports_b_noon where Date BETWEEN %s AND %s GROUP by Date"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        date4.append(row)

    return result4, date4


# plotting the line 1 points
result1, date1 = read_reports(conn)
plt.plot(date1, result1, label="goose")

# plotting the line 2 points
result2, date2 = read_b(conn)
plt.plot(date2, result2, label="goose.b")

# plotting the line 2 points
result3, date3 = read_noon(conn)
plt.plot(date3, result3, label="goose.noon")

# plotting the line 2 points
result4, date4 = read_b_noob(conn)
plt.plot(date4, result4, label="goose.b.noon")

# naming the x axis
plt.xlabel('Date')
# naming the y axis
plt.ylabel('Results')
# giving a title to my graph
plt.title('4 lines on same graph!')

# show a legend on the plot
plt.legend()

# function to show the plot
plt.show()

# fig = go.Figure(data=go.Scatter(x=date1,y=, mode='lines'))
# fig.show()