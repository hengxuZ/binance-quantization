# -*- coding: utf-8 -*-
from app.BinanceAPI import BinanceAPI
from app.authorization import api_key,api_secret
from data.runBetData import RunBetData
from app.dingding import Message
import time

binan = BinanceAPI(api_key,api_secret)
runbet = RunBetData()
msg = Message()

class Run_Main():

    def __init__(self):
        self.coinType = runbet.get_cointype()  # 交易币种
        pass


    def loop_run(self):
        while True:
            cur_market_price = binan.get_ticker_price(runbet.get_cointype()) # 当前交易对市价
            grid_buy_price = runbet.get_buy_price()  # 当前网格买入价格
            grid_sell_price = runbet.get_sell_price() # 当前网格卖出价格
            spot_quantity = runbet.get_spot_quantity()   # 现货买入量
            future_quantity = runbet.get_future_quantity()   # 期货买入量
            spot_step = runbet.get_spot_step() # 当前现货步数
            future_step = runbet.get_future_step() # 当前现货步数
            
            if grid_buy_price >= cur_market_price:   # 是否满足买入价
                
                if future_step != 0: # 说明期货有仓位 则卖出 仓位-1
                    future_res = msg.buy_limit_future_msg(self.coinType,runbet.get_future_quantity(False), grid_buy_price) # 期货卖出
                    if future_res['orderId'] : runbet.set_future_step(future_step - 1) # 挂单成功，仓位 -1 
                    
                res = msg.buy_limit_msg(self.coinType, spot_quantity, grid_buy_price) # 现货买入
                if res['orderId']: # 挂单成功
                    runbet.set_spot_step(spot_step+1)
                    runbet.modify_price(grid_buy_price) #修改data.json中价格、当前步数
                    time.sleep(60*1) # 挂单后，停止运行1分钟
                else:
                    break

            elif grid_sell_price < cur_market_price:  # 是否满足卖出价
                
                if spot_step != 0: # 说明现货有仓位 则卖出 仓位-1
                    spot_res = msg.sell_limit_msg(self.coinType,runbet.get_spot_quantity(False),grid_sell_price) # 期货卖出开多
                    if spot_res['orderId'] : runbet.set_spot_step(spot_step - 1) # 挂单成功，仓位 -1 
  
                future_res = msg.sell_limit_future_msg(self.coinType, future_quantity, grid_sell_price) #期货买入开空
                if future_res['orderId']:
                    runbet.modify_price(grid_sell_price)#修改data.json中价格
                    runbet.set_future_step(future_step+1) 
                    time.sleep(60*1)  # 挂单后，停止运行1分钟
                else:
                    break
            else:
                print("当前市价：{market_price}。未能满足交易,继续运行".format(market_price = cur_market_price))
                time.sleep(2)


# if __name__ == "__main__":
#     instance = Run_Main()
#     try:
#         instance.loop_run()
#     except Exception as e:
#         error_info = "报警：币种{coin},服务停止".format(coin=instance.coinType)
#         msg.dingding_warn(error_info)

#调试看报错运行下面，正式运行用上面       
if __name__ == "__main__":       
    instance = Run_Main()    
    instance.loop_run()
