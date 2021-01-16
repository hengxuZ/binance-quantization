import os,json
# linux
data_path = os.getcwd()+"/data/data.json"
# 本地调试
# data_path = os.getcwd()+""+"/data/data.json"
# windows
# data_path = os.getcwd() + "\data\data.json"

class RunBetData:

    def _get_json_data(self):
        '''读取json文件'''
        tmp_json = {}
        with open(data_path, 'r') as f:
            tmp_json = json.load(f)
            f.close()
        return tmp_json


    def _modify_json_data(self,data):
        '''修改json文件'''
        with open(data_path, "w") as f:
            f.write(json.dumps(data, indent=4))
        f.close()


    ####------下面为输出函数--------####

    def get_buy_price(self):
        data_json = self._get_json_data()
        return data_json["runBet"]["next_buy_price"]


    def get_sell_price(self):
        data_json = self._get_json_data()
        return data_json["runBet"]["grid_sell_price"]

    def get_cointype(self):
        data_json = self._get_json_data()
        return data_json["config"]["cointype"]

    def get_spot_quantity(self,exchange_method=True):
        '''
        :param exchange: True 代表买入，取买入的仓位 False：代表卖出，取卖出应该的仓位
        :return:
        '''

        data_json = self._get_json_data()
        cur_step = data_json["runBet"]["spot_step"] if exchange_method else data_json["runBet"]["spot_step"] - 1 # 买入与卖出操作对应的仓位不同
        quantity_arr = data_json["config"]["spot_quantity"]

        quantity = None
        if cur_step < len(quantity_arr): # 当前仓位 > 设置的仓位 取最后一位
            quantity = quantity_arr[0] if cur_step == 0 else quantity_arr[cur_step]
        else:
            quantity = quantity_arr[-1]
        return quantity

    def get_future_quantity(self,exchange_method=True):
        '''
        :param exchange: True 代表买入，取买入的仓位 False：代表卖出，取卖出应该的仓位
        :return:
        '''

        data_json = self._get_json_data()
        cur_step = data_json["runBet"]["future_step"] if exchange_method else data_json["runBet"]["future_step"] - 1 # 买入与卖出操作对应的仓位不同
        quantity_arr = data_json["config"]["future_quantity"]

        quantity = None
        if cur_step < len(quantity_arr): # 当前仓位 > 设置的仓位 取最后一位
            quantity = quantity_arr[0] if cur_step == 0 else quantity_arr[cur_step]
        else:
            quantity = quantity_arr[-1]
        return quantity

    def get_spot_step(self):
        '''获取现货仓位数'''
        data_json = self._get_json_data()
        return data_json['runBet']['spot_step']

    def get_future_step(self):
        '''获取期货仓位数'''
        data_json = self._get_json_data()
        return data_json['runBet']['future_step']  
     
    def get_profit_ratio(self):
        '''获取补仓比率'''
        data_json = self._get_json_data()
        return data_json['config']['profit_ratio']  
    
    def get_double_throw_ratio(self):
        '''获取止盈比率'''
        data_json = self._get_json_data()
        return data_json['config']['double_throw_ratio']          

    # 买入后，修改 补仓价格 和 网格平仓价格以及步数
    def modify_price(self, deal_price):
        print("开始修改补仓价和网格价")
        data_json = self._get_json_data()
        data_json["runBet"]["next_buy_price"] = round(deal_price * (1 - data_json["config"]["double_throw_ratio"] / 100), 2) # 保留2位小数
        data_json["runBet"]["grid_sell_price"] = round(deal_price * (1 + data_json["config"]["profit_ratio"] / 100), 2)

        self._modify_json_data(data_json)
        print("修改后的补仓价格为:{double}。修改后的网格价格为:{grid}".format(double=data_json["runBet"]["next_buy_price"],
                                                           grid=data_json["runBet"]["grid_sell_price"]))
    def set_future_step(self,future_step):
        '''修改期货仓位数'''
        data_json = self._get_json_data()
        data_json['runBet']['future_step'] = future_step
        self._modify_json_data(data_json)
        
    def set_spot_step(self,spot_step):
        '''修改期货仓位数'''
        data_json = self._get_json_data()
        data_json['runBet']['spot_step'] = spot_step
        self._modify_json_data(data_json)

if __name__ == "__main__":
    instance = RunBetData()
    # print(instance.modify_price(8.87,instance.get_step()-1))
    print(instance.get_future_quantity())
