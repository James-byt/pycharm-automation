<<<<<<< Updated upstream
import talib
from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np
import pyodbc
from datetime import date
=======
>>>>>>> Stashed changes



def daily_balance(conn):
    balance = []
    cursor = conn.cursor()
    cursor.execute("select balance from Trades")
    records = cursor.fetchall()
    for row in records:
        balance = row[-1]
    new_balance = balance
    return new_balance


<<<<<<< Updated upstream
def calculate(balance):
    Amount = (balance * 7 / 100) // 5
    return Amount
=======
#def calculate(balance):
  #  Amount = (balance * 10 / 100) // 5
  #  return Amount`
>>>>>>> Stashed changes


def set_new_amount(conn, new_amount):
    cursor = conn.cursor()
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 0))
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 1))
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 2))
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 3))
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 4))
    conn.commit()


<<<<<<< Updated upstream
from iqoptionapi.stable_api import IQ_Option
API = IQ_Option("debeilarh@gmail.com", "0828383312iq")
API.connect()  # connect to iqoption
MODE ="PRACTICE"
API.change_balance(MODE)
new_money = 10
goal="EURUSD"
size=1 #size=[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all"]
maxdict=10
print("start stream...")
API.start_candles_stream(goal,size,maxdict)
#DO something
print("Do something...")
time.sleep(10)
first = 1
second = 2

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
    print("print candles")
    candles=API.get_realtime_candles(goal,size)
    for k in candles:
        print(goal,"size",k,candles[k])
    print("stop candle")
    API.stop_candles_stream(goal,size)

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


    #current_sar = sar[-1]
    current_rsi = rsi_list[first]
    #current_stoch = slowk_list[-1]
    second_last_rsi = rsi_list[second]
    #second_lats_stoch = slowk_list[-2]
    open_price = inputs['open']
    #open_price = inputs['open']
    current_open = open_price[first]


    print("rsi ", current_rsi)
    #print("Stock ", current_stoch)
    #print("sar", current_sar)
    #print("open", current_open)
    print("indicators send")
    print("\n")
    time.sleep(1)
    return current_rsi, second_last_rsi


# create model()
# NB: You need to use the currents prices and numbers
def buy_order_zone():
    buy_zone = 0
    rsi_lower = 25
    stoch_lower = 20
    current_rsi, second_last_rsi, current_sar = stream()

    if buy_zone == 1 and second_last_rsi <= rsi_lower: #and second_lats_stoch <= stoch_lower:
        buy_zone = 2
        print("2nd buy zone")
    if buy_zone == 2 and current_rsi >= rsi_lower: #and current_stoch >= stoch_lower:
        buy_zone = 3
        print("3rd buy zone sent")
    else:
        print("no buy zones")
    return buy_zone


def sell_order_zone():
    sell_zone = 0
    rsi_upper = 75
    stoch_upper = 80
    current_rsi, second_last_rsi = stream()

    if sell_zone == 1 and second_last_rsi > rsi_upper: #and second_lats_stoch > stoch_upper:
        sell_zone = 2
        print("2nd sell zone")
    if sell_zone == 2 and current_rsi <= rsi_upper: #and current_stoch <= stoch_upper:
        sell_zone = 3
        print("3rd sell zone send")
    else:
        print("no sell zones")
    return sell_zone


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
=======

#new_amount = calculate(balance)

#set_new_amount(conn, new_amount)
>>>>>>> Stashed changes

    trade += 1
    first += 1
    second += 1
API.stop_candles_stream(goal, size)
conn.close()
print("Reached trade limit")
