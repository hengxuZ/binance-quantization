from app.BinanceAPI import BinanceAPI
from app.authorization import api_key,api_secret
from data.runBetData import RunBetData
from app.dingding import Message
import time

binan = BinanceAPI(api_key,api_secret)
runbet = RunBetData()
msg = Message()


# 运行该文件 必须申请钉钉机器人，将token填入authorization中
def loop_fun():
    while True:
        if runbet.get_buy_price() >= binan.get_ticker_price(runbet.get_cointype()):
            order_id = msg.buy_limit_msg(runbet.get_cointype(),runbet.get_quantity(),runbet.get_buy_price())
            if order_id['orderId']:
                runbet.modify_price(runbet.get_buy_price(),runbet.get_step()+1)
                time.sleep(60) # 挂单后，停止运行1分钟

        elif runbet.get_sell_price() < binan.get_ticker_price(runbet.get_cointype()):

            order_id = msg.sell_limit_msg(runbet.get_cointype(),runbet.get_quantity(), runbet.get_sell_price())
            if order_id['orderId']:
                runbet.modify_price(runbet.get_sell_price(),runbet.get_step()-1)
                time.sleep(60)
        else:
            print("当前市价：{market_price}。未能满足交易,继续运行".format(market_price = binan.get_ticker_price(runbet.get_cointype())))


if __name__ == "__main__":
    try:
        loop_fun()
    except Exception as e:
        error_info = "报警：" + str(e)
        msg.dingding_warn(error_info)