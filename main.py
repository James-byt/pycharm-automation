import talib
from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np

print("login...")
I_want_money = IQ_Option("debeilahlabirwa@gmail.com", "12345678i")
I_want_money.connect()  # connect to iqoption
goal = "EURUSD-OTC"
size = 900  # size=[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all"]
#timeperiod = 15 #
maxdict = 20 #number of candele stick
print("start stream...")
I_want_money.start_candles_stream(goal, size, maxdict)
print("Start EMA Sample")
while True:

    candles = I_want_money.get_realtime_candles(goal, size)

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


    print("Show RSi")
    rsi = talib.RSI(inputs["close"],  timeperiod=4)
    slowk, slowd = talib.STOCH(inputs["high"], inputs["low"], inputs["close"], fastk_period=5, slowk_period=1,
                               slowk_matype=1, slowd_period=1,
                             slowd_matype=1)

    sar = talib.SAR(inputs["high"], inputs["low"], acceleration=0.02, maximum=0.2)
    open_price = inputs['open']
    print(sar[-1])
    print(rsi[-1])
    print(open_price[-1])
    time.sleep(1)
I_want_money.stop_candles_stream(goal, size)