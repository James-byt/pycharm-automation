import talib
from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np
import mysql.connector
#import pyodbc
from datetime import date

# retrieve matrix from database into

conn = mysql.connector.connect(
        user="root",
        host="localhost",
        database="golden"
    )


def retrieve_matrix(conn):
    print()
    cursor = conn.cursor()
    cursor.execute("select * from goose_b_noon")
    records = cursor.fetchall()
    for row in records:
        matrix.append(row)
    print("retieved matrix",matrix)


def add_submatrix(conn):
    print("Create")

    cursor = conn.cursor()
    sql = "INSERT INTO goose_b_noon (a,b,c) VALUES (%s, %s, %s)"
    val = (store_action[0], store_action[1],store_action[2])
    cursor.execute(sql, val)

    conn.commit()


def delete_submatrix(conn):
    print("Delete")
    cursor = conn.cursor()
    cursor.execute(
        'delete from goose_b_noon LIMIT 1'
    )
    conn.commit()


# afternoon
matrix = []
retrieve_matrix(conn)

stop_number = 0
while stop_number < 3:

    # Currency = AUDUSD

    #print("login...")
    API = IQ_Option("debeilarh@gmail.com", "0828383312iq")
    API.connect()  # connect to iqoption
    MODE = "PRACTICE"  # PRACTICE or REAL
    API.change_balance(MODE)
    goal = "EURUSD"  # NZDUSD EURJPY AUDUSD
    new_money = 10

    size = 60  # size=[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all"]
    timeperiod = 15  #
    maxdict = 20  # number of candele sticks
    #print("start stream...")
    API.start_candles_stream(goal, size, maxdict)
    #print("Start RSI & Stoch Sample")

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

        rsi_list = talib.RSI(inputs["close"], timeperiod=4)
        slowk_list, slowd_list = talib.STOCH(inputs["high"], inputs["low"], inputs["close"], fastk_period=5,
                                             slowk_period=1, slowk_matype=0, slowd_period=1,
                                             slowd_matype=0)
        sar = talib.SAR(inputs["high"], inputs["low"], acceleration=0.02, maximum=0.2)

        current_sar = sar[-1]
        current_rsi = rsi_list[-1]
        current_stoch = slowk_list[-1]
        second_last_rsi = rsi_list[-2]
        second_lats_stoch = slowk_list[-2]
        third_last_rsi = rsi_list[-3]
        third_lats_stoch = slowk_list[-3]
        open_price = inputs['open']
        current_open = open_price[-1]

        #print("rsi ", current_rsi)
        #print("Stock ", current_stoch)
        #print("sar", current_sar)
        #print("open", current_open)
        #print("indicators send")
        #print("\n")
        time.sleep(1)
        return current_rsi, current_stoch, second_last_rsi, second_lats_stoch, current_sar, current_open, third_last_rsi, third_lats_stoch


    def trade_calculation():
        trades_value = np.average(matrix, axis=0)
        for value in trades_value:
            if value > 0:
                trades.append("call")
            elif value < 0:
                trades.append("put")

        return trades


    def store_results(action, results):

        if results < 0 and action == "put":
            action = 1  # call
            store_action.append(action)
        elif results < 0 and action == "call":
            action = -1
            store_action.append(action)
        if results > 0 and action == "put":
            action = -1
            store_action.append(action)
        elif results > 0 and action == "call":
            action = 1
            store_action.append(action)

        return store_action


    # create model()
    # NB: You need to use the currents prices and numbers
    def below_order_zone():  # Trades that are above the (>)RSI
        below_zone = 0
        rsi_lower = 25
        stoch_lower = 20
        current_rsi, current_stoch, second_last_rsi, second_lats_stoch, current_sar, current_open, third_last_rsi, third_lats_stoch = stream()

        if below_zone == 0 and second_last_rsi <= rsi_lower: #and second_lats_stoch <= stoch_lower:
            below_zone = 1
            #print("1st sell zone")
        if below_zone == 1 and third_last_rsi >= rsi_lower: #and third_lats_stoch >= stoch_lower:
            below_zone = 2
            #print("2nd sell zone")



        #else:

            #print("no sell zones")
        return below_zone

    # buy/buy
    #print("looking for trades")
    trades = []
    balance = API.get_balance()
    trades = trade_calculation()
    store_action = []
    for action in trades:
        keep_trading = True
        while keep_trading:
            # new_money = read(conn)
            #above_zone = 0
            below_zone = below_order_zone()
            amount = new_money
            ACTIVES = goal
            duration = 1
            stop_number += 1
            if below_zone == 2:
                #print("below zone")
                _, id = API.buy_digital_spot(ACTIVES, amount, action, duration)
                while True:
                    check, _ = API.check_win_digital_v2(id)
                    if check:
                        break
                status = API.check_win_digital_v2(id)
                bol, results = status
                #create(conn, results)
                #print("Trade results:", action, results)
                # store_results(action, results)
                time.sleep(5)
                # dfhistoruy["Order"] "Bull" store orders
                # df["Results"] store results
                break

            # else:
            # print("looking for trades")
    matrix.append(store_action)
    matrix.remove(matrix[0])
    API.stop_candles_stream(goal, size)
    print("|||||||||||||||||||||||||||||||||||||3 trades made profit/loss: ???? ||||||||||||||||||||||||||||||||||||||")

    # matrix must be the same in database
    print(matrix)

    # store matrix back in database
    add_submatrix(conn)
    delete_submatrix(conn)