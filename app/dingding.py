# author-wechat：findpanpan

import requests,json

# windows
# from app.authorization import dingding_token, recv_window,api_secret,api_key
# from app.BinanceAPI import BinanceAPI
# linux
from app.BinanceAPI import BinanceAPI
from app.authorization import dingding_token, recv_window,api_secret,api_key

class Message:

    def buy_limit_msg(self,market, quantity, rate):
        '''
        现货卖出带有钉钉消息的封装
        :param market:
        :param quantity: 数量
        :param rate: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key,api_secret).buy_limit(market, quantity, rate)
            if res['orderId']:
                buy_info = "报警：币种为：{cointype}。买单价为：{price}。买单量为：{num}".format(cointype=market,price=rate,num=quantity)
                self.dingding_warn(buy_info)
                return res
        except BaseException as e:
            error_info = "报警：币种为：{cointype},买单失败.api返回内容为:{reject}".format(cointype=market,reject=res['msg'])
            self.dingding_warn(error_info)


    def sell_limit_msg(self,market, quantity, rate, profit_usdt=0):
        '''
        现货卖出带有钉钉消息的封装
        :param market:
        :param quantity: 数量
        :param rate: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key,api_secret).sell_limit(market, quantity, rate)
            if res['orderId']:
                buy_info = "报警：币种为：{cointype}。卖单价为：{price}。卖单量为：{num}.盈利usdt数为:{profit_usdt}".format(cointype=market,price=rate,num=quantity,profit_usdt=profit_usdt)
                self.dingding_warn(buy_info)
                return res
        except BaseException as e:
            error_info = "报警：币种为：{cointype},卖单失败.api返回内容为:{reject}".format(cointype=market,reject=res['msg'])
            self.dingding_warn(error_info+str(res))
            return res

    def sell_limit_future_msg(self,market, quantity, price):
        '''
        合约做空单，带有钉钉消息
        :param market: 交易对
        :param quantity: 数量
        :param price: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key,api_secret).limit_future_order('SELL', market, quantity, price)
            if res['orderId']:
                buy_info = "报警：币种为：{cointype}。卖出做空价格为：{price}。数量为：{num}".format(cointype=market,price=price,num=quantity)
                self.dingding_warn(buy_info)
                return res
        except BaseException as e:
            error_info = "报警：币种为：{cointype},卖出做空空单失败.api返回内容为:{reject}".format(cointype=market,reject=res['msg'])
            self.dingding_warn(error_info+str(res))
            return res
        
    def buy_limit_future_msg(self,market, quantity, price,profit_usdt=None):
        '''
        合约做多单，带有钉钉消息
        :param market: 交易对
        :param quantity: 数量
        :param price: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key,api_secret).limit_future_order('BUY', market, quantity, price)
            if res['orderId']:
                buy_info = "报警：币种为：{cointype}。买入做多价格为：{price}。数量为：{num}。盈利USDT数为:{profit_usdt}".format(cointype=market,price=price,num=quantity,profit_usdt=profit_usdt)
                self.dingding_warn(buy_info)
                return res
        except BaseException as e:
            error_info = "报警：币种为：{cointype},卖出空单失败.api返回内容为:{reject}".format(cointype=market,reject=res['msg'])
            self.dingding_warn(error_info+str(res))
            return res
        
    def dingding_warn(self,text):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        api_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % dingding_token
        json_text = self._msg(text)
        requests.post(api_url, json.dumps(json_text), headers=headers).content

    def _msg(self,text):
        json_text = {
            "msgtype": "text",
            "at": {
                "atMobiles": [
                    "11111"
                ],
                "isAtAll": False
            },
            "text": {
                "content": text
            }
        }
        return json_text

if __name__ == "__main__":
    msg = Message()
    print(msg.buy_limit_future_msg("EOSUSDT",3,2))