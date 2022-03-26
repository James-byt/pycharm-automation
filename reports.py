# Scripts for weekly progress reports per currency(bar graph) + allocated amount(Pie chart) + Balance vs daily target (double bar graph)
# Scripts for daily progress reports per currency(bar graph) + allocated amount(Pie chart) + Balance vs daily target (double bar graph)

import pyodbc
import matplotlib.pyplot as plt

from datetime import datetime

conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=DESKTOP-QMIE1ES;"
    "Database=golden;"
    "Trusted_Connection=yes;")


def read_allocated(conn):
    trade_days = 1
    new_amount = []
    currency = []
    cursor = conn.cursor()
    cursor.execute("select * from Amounts ")
    # records = cursor.fetchall()
    for row in cursor:
        new_amount.append(row[2] * trade_days)
        currency.append(row[1])
    amount = new_amount
    currency_pairs = currency
    return amount, currency_pairs


def read_results(conn):
    date_from_str = "18/02/22"
    date_from = datetime.strptime(date_from_str, '%d/%m/%y')
    date_to_str = "18/02/22"
    date_to = datetime.strptime(date_to_str, '%d/%m/%y')
    new_results = []
    currency = []
    cursor = conn.cursor()
    cursor.execute("select Currency, sum(Results) from Trades where Date BETWEEN ? AND ? GROUP BY Currency",
                   (date_from, date_to))

    records = cursor.fetchall()
    for row in records:
        new_results.append(row[1])
        currency.append(row[0])
    results = new_results
    currency_results = currency
    return currency_results, results


def read_overall(conn):
    date_from_str = "18/02/22"
    date_from = datetime.strptime(date_from_str, '%d/%m/%y')
    date_to_str = "18/02/22"
    date_to = datetime.strptime(date_to_str, '%d/%m/%y')
    overall_results = 0
    cursor = conn.cursor()
    cursor.execute("select sum(Results) from Trades where Date BETWEEN ? AND ?", (date_from, date_to))
    for row in cursor:
        overall_results = row[0]
    overall = overall_results
    return overall


def calculate_win(conn, amount, results):
    win_percent = []
    for win in results:
        if win < 0:
            win = 0
        win_percent.append(win/amount[0] * 100)
    win_percent = win_percent
    return win_percent


def addlabels(y):
    for index, value in enumerate(y):
        plt.text(index, value, str(value))


#Daily trade progress
currency_results, results = read_results(conn)
negative = []
positive = []
for value in results:
    if value > 0:
        positive.append(value)
    elif value < 0:
        negative.append(value)
positive = positive
negative = negative

fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.bar(currency_results, results)
addlabels(results)
plt.show()

# Overall results

overall = read_overall(conn)
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
x = ["Overall Results"]
ax.bar(x, overall)
plt.text(0, overall, str(overall))
plt.show()

# % win amount
amount, currency_pairs = read_allocated(conn)
win_percent = calculate_win(conn, amount, results)
new_percent = []
for rounded in win_percent:
    new_percent.append(round(rounded))
win_percent = new_percent
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.bar(currency_results, win_percent)
addlabels(win_percent)
plt.show()

# % win

plt.pie(win_percent,
       labels=currency_pairs,
        autopct='%1.1f%%')
plt.title(f'Allocated amount breakdown from {amount[0]} which is 10% of balance')
plt.axis('equal')
plt.show()