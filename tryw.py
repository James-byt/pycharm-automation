import talib
from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np
import pyodbc
from datetime import date


Iq = IQ_Option("debeilarh@gmail.com", "0828383312iq")
Iq.connect()  # connect to iqoption
MODE ="PRACTICE"
Iq.change_balance(MODE)

end_from_time=time.time()
ANS=[]
for i in range(70):
    data=Iq.get_candles("EURUSD", 60, 10, end_from_time)
    ANS =data+ANS
    end_from_time=int(data[0]["from"])-1
print(ANS)