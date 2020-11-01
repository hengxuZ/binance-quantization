# -*- coding: utf-8 -*

from app.BinanceAPI import BinanceAPI
from app.authorization import api_key,api_secret
from data.runBetData import RunBetData
import time

binan = BinanceAPI(api_key,api_secret)
runbet = RunBetData()

# def loop_fun():
#     while True:
#         if runbet.get_buy_price() >= binan.get_ticker_price(runbet.get_cointype()):
#             order_id = binan.buy_limit(runbet.get_cointype(),runbet.get_quantity(),runbet.get_buy_price())
#             runbet.modify_price(runbet.get_buy_price(),runbet.get_step()+1)
#             time.sleep(60*3) # 挂单后，停止运行3分钟

#         elif runbet.get_sell_price() < binan.get_ticker_price(runbet.get_cointype()):
#             order_id = binan.sell_limit(runbet.get_cointype(),runbet.get_quantity(), runbet.get_sell_price())
#             runbet.modify_price(runbet.get_sell_price(),runbet.get_step()-1)
#             time.sleep(60*3) # 吃单后，停止运行3分钟
#         else:
#             print("当前 {cointype} 市价：{market_price}。未能满足交易,继续运行".format(cointype=runbet.get_cointype()[:-4],market_price = binan.get_ticker_price(runbet.get_cointype())))
#             time.sleep(1)


if __name__ == "__main__":
    # try:
    #     loop_fun()
    # except Exception as e:
    #     print(str(e))
    print(binan.get_klines("WINGUSDT"))