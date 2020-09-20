import requests,json

# windows
from app.authorization import dingding_token, recv_window,api_secret,api_key
from app.BinanceAPI import BinanceAPI
# linux
# from app.authorization import dingding_token

class Message:

    def buy_limit_msg(self,market, quantity, rate):
        res = BinanceAPI(api_key,api_secret).buy_limit(market, quantity, rate)
        buy_info = "报警：币种为：{cointype}。买单价为：{price}。买单量为：{num}".format(cointype=market,price=rate,num=quantity)
        self.dingding_warn(buy_info)
        return res

    def sell_limit_msg(self,market, quantity, rate):
        res = BinanceAPI(api_key,api_secret).sell_limit(market, quantity, rate)
        buy_info = "报警：币种为：{cointype}。卖单价为：{price}。卖单量为：{num}".format(cointype=market,price=rate,num=quantity)
        self.dingding_warn(buy_info)
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
    print(msg.buy_limit_msg("EOSUSDT",10,2))