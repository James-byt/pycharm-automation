import pyodbc

conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=DESKTOP-QMIE1ES;"
    "Database=golden;"
    "Trusted_Connection=yes;")


def daily_balance(conn):
    balance = []
    cursor = conn.cursor()
    cursor.execute("select balance from Trades")
    records = cursor.fetchall()
    for row in records:
        balance = row[-1]
    new_balance = balance
    return new_balance


def calculate(balance):
    Amount = (balance * 10 / 100) // 5
    return Amount


def set_new_amount(conn, new_amount):
    cursor = conn.cursor()
    cursor.execute("update Amounts set Amount = ? where App_No = ? ", (new_amount, 0))
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 1))
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 2))
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 3))
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 4))
    conn.commit()
    

balance = daily_balance(conn)

new_amount = calculate(balance)

set_new_amount(conn, new_amount)

print(new_amount)