### data.json配置文件详细解读
> 使用json文件存储数据，目的是不用使用数据库，让门槛更低、更快捷执行策略


- next_buy_price
假设 我要做UNI的网格策略，当前UNI/USDT=40
next_buy_price意味着我买入UNI的价格，我设置为38，当uni跌到了38。就会触发买入指令（v2版本会判断是否最佳买入点 浮动买入，最终买入价低于38）

- grid_sell_price:代表卖出价。
假设设置为42.当价格到达了42则触发卖出指令。v2版本会判断是否最佳买入点 浮动买入，最终买入价高于42）前提你当前账户拥有uni。如果没有uni，那么next_buy_price、grid_sell_price的值都会往上浮动，这样避免价格踏出网格区间

- step：代表 当前 我买了几次UNI了。
比方说uni=40，跌到了38触发第一次买入，step=1，grid_buy_price自动变化成了36。当价格达到36，再次触发买入，step=2。当价格回升满足卖出，那么step=1。

- profit_ratio：代表卖出价格上升的比率
假设profit_ratio设置为10，当grid_sell_price=40被触发后，grid_sell_price = 40 * 1.1 = 44

- double_throw_ratio：代表买入价格下降的比率
假设double_throw_ratio设置为10，当grid_buy_price=40被触发后，grid_sell_price = 40 * （100-10）*0.01 = 36

- quantity：代表你要买入的量。
假设quantity=[10]，当满足买入时，会买入10个uni。当价格继续下跌，当第二次满足买入时，又会买入10个uni。
当数组只有一个值时：任何时候买卖的数量都为该值。
假设quantity=[10,20,30]，当满足买入时，会买入10个uni。当价格继续下跌，当第二次满足买入时，又会买入20个uni。当第三次满足买入时，又会买入30个uni。当第四次满足买入时，会买入30个uni。当第n次满足买入时，会买入30个uni。卖出时，也会按照买入的量卖出。
**注意事项**
由于大多数交易对仅支持最小开仓费用10U。那么在设置quantity的过程中，需要手动计算下最小的买入量，必须大于这个量才行。

计算花费U的公式：UNI价格 * quantity = 花费的U数(一定要大于10)

## 实战举例：
data.json配置如下：
```
{
    "runBet": {
        "next_buy_price":36,      
        "grid_sell_price": 44    
        "step":0                  
    },
    "config": {
        "profit_ratio": 10,         
        "double_throw_ratio": 10,   
        "cointype": "UNIUSDT",   
        "quantity": [10,20,30]        
    }
}
```
现在行情大跌，假设UNI跌到了36，触发了买入价格。data.json自动变成了以下配置：并且买入了10个UNI
```
{
    "runBet": {
        "next_buy_price":32.4,      
        "grid_sell_price": 39.6    
        "step":1                  
    },
    "config": {
        "profit_ratio": 10,         
        "double_throw_ratio": 10,   
        "cointype": "UNIUSDT",   
        "quantity": [10,20,30]        
    }
}
```
现在行情继续下跌，假设UNI跌到了32.4，触发了买入价格。data.json自动变成了以下配置：并且买入了20个UNI
```
{
    "runBet": {
        "next_buy_price":29.16,      
        "grid_sell_price": 35.64    
        "step":2                  
    },
    "config": {
        "profit_ratio": 10,         
        "double_throw_ratio": 10,   
        "cointype": "UNIUSDT",   
        "quantity": [10,20,30]        
    }
}
```
现在行情回升，假设UNI上到了35.64，触发了卖入价格。data.json自动变成了以下配置：并且卖入了20个UNI
```
{
    "runBet": {
        "next_buy_price":32.076,      
        "grid_sell_price": 39.204    
        "step":1                  
    },
    "config": {
        "profit_ratio": 10,         
        "double_throw_ratio": 10,   
        "cointype": "UNIUSDT",   
        "quantity": [10,20,30]        
    }
}
```
