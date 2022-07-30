#import pyodbc
import matplotlib.pyplot as plt
from datetime import datetime
import mysql.connector


conn = mysql.connector.connect(
        user="root",
        host="localhost",
        database="golden"
    )


def read_overall(conn):
    date_from_str = "20/07/22"
    date_from = datetime.strptime(date_from_str, '%d/%m/%y')
    date_to_str = "20/07/22"
    date_to = datetime.strptime(date_to_str, '%d/%m/%y')
    cursor = conn.cursor()

    sql = "select sum(Results) from reports where Date BETWEEN %s AND %s"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        result1 = row[0]

    sql = "select sum(Results) from reports_b where Date BETWEEN %s AND %s"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        result2 = row[0]

    sql = "select sum(Results) from reports_noon where Date BETWEEN %s AND %s"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        result3 = row[0]

    sql = "select sum(Results) from reports_b_noon where Date BETWEEN %s AND %s"
    val = (date_from, date_to)
    cursor.execute(sql, val)
    for row in cursor:
        result4 = row[0]

    return result1, result2, result3, result4


# Overall results
result1, result2, result3, result4 = read_overall(conn)

# x-coordinates of left sides of bars
left = [1, 2, 3, 4]

# heights of bars
height = [result1, result2, result3, result4]

# labels for bars
tick_label = ['goose', 'goose.b', 'goose.noon', 'goose.b.noon']

# plotting a bar chart
plt.bar(left, height, tick_label=tick_label,
        width=0.8, color=['red', 'green'])

# naming the x-axis
plt.xlabel('x - axis')
# naming the y-axis
plt.ylabel('y - axis')
# plot title
plt.title('My bar chart!')

# function to show the plot
plt.imsave