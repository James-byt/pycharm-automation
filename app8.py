import talib
from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np
import pyodbc
from datetime import date


print("login...")
API = IQ_Option("debeilarh@gmail.com", "0828383312iq")
API.connect()  # connect to iqoption
MODE = "REAL"
API.change_balance(MODE)
goal = "USDCHF"
new_money = 10

size = 900  # size=[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all"]
timeperiod = 15  #
maxdict = 20  # number of candele sticks
print("start stream...")
API.start_candles_stream(goal, size, maxdict)
print("Start RSI & Stoch Sample")

conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=DESKTOP-QMIE1ES;"
    "Database=golden;"
    "Trusted_Connection=yes;"
)


def read(conn):
    cursor = conn.cursor()
    cursor.execute("select * from Amounts where App_No = 0 ")
    records = cursor.fetchall()
    for row in records:
        new_money = row[2]
    return new_money


def create(conn, results):
    today = date.today()
    balance = API.get_balance()
    print("Create")
    cursor = conn.cursor()
    cursor.execute(
        'insert into Trades( Currency, Date, Results, Balance) values(?,?,?,?);',
        (goal, today, results, balance)
    )
    conn.commit()
    read(conn)


def stream():
    # while True:
    candles = API.get_realtime_candles(goal, size)

    inputs = {
        'open': np.array([]),
        'high': np.array([]),
        'low': np.array([]),
        'close': np.array([]),
        'volume': np.array([]),

    }
    for timestamp in candles:
        inputs["open"] = np.append(inputs["open"], candles[timestamp]["open"])
        inputs["high"] = np.append(inputs["high"], candles[timestamp]["max"])
        inputs["low"] = np.append(inputs["low"], candles[timestamp]["min"])
        inputs["close"] = np.append(inputs["close"], candles[timestamp]["close"])
        inputs["volume"] = np.append(inputs["volume"], candles[timestamp]["volume"])

    rsi_list = talib.RSI(inputs["close"], timeperiod=3)
    slowk_list, slowd_list = talib.STOCH(inputs["high"], inputs["low"], inputs["close"], fastk_period=4, slowk_period=1,
                                         slowk_matype=0, slowd_period=1,
                                         slowd_matype=0)
    sar = talib.SAR(inputs["high"], inputs["low"], acceleration=0.02, maximum=0.2)

    current_sar = sar[-1]
    current_rsi = rsi_list[-1]
    current_stoch = slowk_list[-1]
    second_last_rsi = rsi_list[-2]
    second_lats_stoch = slowk_list[-2]
    open_price = inputs['open']
    current_open = open_price[-1]

    print("rsi ", current_rsi)
    print("Stock ", current_stoch)
    print("sar", current_sar)
    print("open", current_open)
    print("indicators send")
    print("\n")
    time.sleep(1)
    return current_rsi, current_stoch, second_last_rsi, second_lats_stoch, current_sar, current_open


# create model()
# NB: You need to use the currents prices and numbers
def buy_order_zone():
    buy_zone = 0
    rsi_lower = 25
    stoch_lower = 20
    current_rsi, current_stoch, second_last_rsi, second_lats_stoch, current_sar, current_open = stream()
    if current_sar < current_open:
        buy_zone = 1
        print("1st buy zone")
    if buy_zone == 1 and second_last_rsi <= rsi_lower and second_lats_stoch <= stoch_lower:
        buy_zone = 2
        print("2nd buy zone")
    if buy_zone == 2 and current_rsi >= rsi_lower and current_stoch >= stoch_lower:
        buy_zone = 3
        print("3rd buy zone sent")
    else:
        print("no buy zones")
    return buy_zone


def sell_order_zone():
    sell_zone = 0
    rsi_upper = 75
    stoch_upper = 80
    current_rsi, current_stoch, second_last_rsi, second_lats_stoch, current_sar, current_open = stream()
    if current_sar > current_open:
        sell_zone = 1
        print("1st sell zone")
    if sell_zone == 1 and second_last_rsi > rsi_upper and second_lats_stoch > stoch_upper:
        sell_zone = 2
        print("2nd sell zone")
    if sell_zone == 2 and current_rsi <= rsi_upper and current_stoch <= stoch_upper:
        sell_zone = 3
        print("3rd sell zone send")
    else:
        print("no sell zones")
    return sell_zone


# buy/buy
print("looking for trades")
trade = 0
balance = API.get_balance()
while trade < 1:
    keep_trading = True
    while keep_trading:
        # new_money = read(conn)
        buy_zone = buy_order_zone()
        sell_zone = sell_order_zone()
        if buy_zone == 3 or sell_zone == 3:
            print("first wall")
            Money = new_money
            ACTIVES = goal
            ACTION = "call"  # or "put"Academic Transcript
            expirations_mode = 15
            if buy_zone == 3:
                print("buy wall")
                check, id = API.buy(Money, ACTIVES, "call", expirations_mode)
                results = API.check_win_v3(id)
                print("buy")
                create(conn, results)
                # time.sleep(300)
                # dfhistoruy["Order"] "Bull" store orders
                # df["Results"] store results
                break
            elif sell_zone == 3:  # store orders
                print("sell wall")
                check, id = API.buy(Money, ACTIVES, "put", expirations_mode)
                results = API.check_win_v3(id)
                print("sell")
                create(conn, results)
                # dfhistory["Order"] = "Sell price + rsi at sell + stoch at sell + win/loss
                break
        # else:
        # print("looking for trades")

    trade += 1
API.stop_candles_stream(goal, size)
conn.close()
print("Reached trade limit")
