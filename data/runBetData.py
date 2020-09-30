import os,json
# linux
# data_path = os.getcwd()+"/data/data.json"
# windows
data_path = os.getcwd() + "\data\data.json"

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

    def get_quantity(self):
        data_json = self._get_json_data()
        return data_json["config"]["quantity"]

    # 买入后，修改 补仓价格 和 网格平仓价格
    def modify_price(self, deal_price):
        print("交易成功，开始修改补仓价和网格价")
        data_json = self._get_json_data()
        data_json["runBet"]["next_buy_price"] = round(deal_price * (1 - data_json["config"]["double_throw_ratio"] / 100), 4)
        data_json["runBet"]["grid_sell_price"] = round(deal_price * (1 + data_json["config"]["profit_ratio"] / 100), 4)

        self._modify_json_data(data_json)
        print("修改后的补仓价格为:{double}。修改后的网格价格为:{grid}".format(double=data_json["runBet"]["next_buy_price"],
                                                           grid=data_json["runBet"]["grid_sell_price"]))


if __name__ == "__main__":
    instance = RunBetData()
    print(instance.modify_price(0.10245))