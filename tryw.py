from iqoptionapi.stable_api import IQ_Option
Iq = IQ_Option("debeilarh@gmail.com", "0828383312iq")
Iq.connect()  # connect to iqoption
MODE ="PRACTICE"
Iq.change_balance(MODE)
instrument_type="crypto"
instrument_id="EURUSD"
side="buy"#input:"buy"/"sell"
amount=1.23#input how many Amount you want to play

#"leverage"="Multiplier"
leverage=3#you can get more information in get_available_leverages()

type="market"#input:"market"/"limit"/"stop"

#for type="limit"/"stop"

# only working by set type="limit"
limit_price=None#input:None/value(float/int)

# only working by set type="stop"
stop_price=None#input:None/value(float/int)

#"percent"=Profit Percentage
#"price"=Asset Price
#"diff"=Profit in Money

stop_lose_kind="percent"#input:None/"price"/"diff"/"percent"
stop_lose_value=95#input:None/value(float/int)

take_profit_kind=None#input:None/"price"/"diff"/"percent"
take_profit_value=None#input:None/value(float/int)

#"use_trail_stop"="Trailing Stop"
use_trail_stop=True#True/False

#"auto_margin_call"="Use Balance to Keep Position Open"
auto_margin_call=False#True/False
#if you want "take_profit_kind"&
#            "take_profit_value"&
#            "stop_lose_kind"&
#            "stop_lose_value" all being "Not Set","auto_margin_call" need to set:True

use_token_for_commission=False#True/False
print("buy")

Iq.buy_order(
            instrument_type="forex", instrument_id="USDJPY",
            side="sell", amount=1, leverage=200,
            type="market", limit_price=None, stop_price=None,
            stop_lose_kind=None,
            stop_lose_value=None,
            take_profit_kind=None,
            take_profit_value=None,
            use_trail_stop=False, auto_margin_call=False,
            use_token_for_commission=False)
print("buy")
