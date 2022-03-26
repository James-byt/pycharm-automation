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
    Amount = (balance * 7 / 100) // 5
    return Amount


def set_new_amount(conn, new_amount):
    cursor = conn.cursor()
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 0))
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 1))
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 2))
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 3))
    cursor.execute("update Amounts set Amount = ? where App_No = ? ; ", (new_amount, 4))
    conn.commit()


from iqoptionapi.stable_api import IQ_Option
API = IQ_Option("debeilarh@gmail.com", "0828383312iq")
API.connect()  # connect to iqoption
MODE ="PRACTICE"
API.change_balance(MODE)
actives = "EURUSD"
duration = 5  # minute 1 or 5
action = "put"  # put
instrument_type ="forex"

instrument_id="EURUSD"
side="buy"
amount= 1.23  #input how many Amount you want to play

#"leverage"="Multiplier"
leverage=50 #you can get more information in get_available_leverages()

type="market" #input:"market"/"limit"/"stop"

#for type="limit"/"stop"

# only working by set type="limit"
limit_price=None#input:None/value(float/int)
# only working by set type="stop"
stop_price=None#input:None/value(float/int)

#"percent"=Profit Percentage
#"price"=Asset Price
#"diff"=Profit in Money

stop_lose_kind="percent"#input:None/"price"/"diff"/"percent"
stop_lose_value=50#input:None/value(float/int)

take_profit_kind="percent"#input:None/"price"/"diff"/"percent"
take_profit_value=70#input:None/value(float/int)

#"use_trail_stop"="Trailing Stop"
use_trail_stop=True#True/False

#"auto_margin_call"="Use Balance to Keep Position Open"
auto_margin_call=False#True/False
#if you want "take_profit_kind"&
#            "take_profit_value"&
#            "stop_lose_kind"&
#            "stop_lose_value" all being "Not Set","auto_margin_call" need to set:True

use_token_for_commission=False#True/False

API.buy_order(
            instrument_type=instrument_type, instrument_id=instrument_id,
            side=side, amount=amount,leverage=leverage,
            type=type,limit_price=limit_price, stop_price=stop_price,
            stop_lose_kind=stop_lose_kind,
            stop_lose_value=stop_lose_value,
            take_profit_kind=take_profit_kind,
            take_profit_value=take_profit_value,
            use_trail_stop=use_trail_stop, auto_margin_call=auto_margin_call,
            use_token_for_commission=use_token_for_commission)

#print(API.get_order(order_id))
#print(I_want_money.get_positions("crypto"))
#print(I_want_money.get_position_history("crypto"))
#print(I_want_money.get_available_leverages("crypto","BTCUSD"))
#print(I_want_money.close_position(order_id))
#print(I_want_money.get_overnight_fee("crypto","BTCUSD"))


#print(API.get_available_leverages(instrument_type,actives))
