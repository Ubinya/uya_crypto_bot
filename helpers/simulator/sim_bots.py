import os
import sys
from pprint import pprint
import time
import logging
# import backtrader as bt
import numpy as np
from decimal import Decimal
import json
# from binance.lib.utils import config_logging
from utils import *

class BotManager(object):
    def __init__(self):
        logging.info('[模拟姬]给狗修金大人请安~准备开始本次调教(调试)了!!')
        self.bot_list = []

    def add_grid_bot(self, symbol, price_mode, price_diff, max_order, fund_each):
        insbot = grid_bot(symbol, price_mode, price_diff, max_order, fund_each)
        self.bot_list.append(insbot)

    def add_balancer_bot(self, qty, multiple, diff):# init coin qty,(asset value / total value),least order value
        insbot = balancer_bot(qty, multiple, diff)
        self.bot_list.append(insbot)

    def run_init(self):
        self.bot_num = len(self.bot_list)
        logging.info("模拟分姬数:{}".format(self.bot_num))

    def do_manager_loop(self):
        with open('BotManager.json', 'w') as f:
            save = {'status': "running", 'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), }
            json_str = json.dumps(save)
            f.write(json_str)
        for bot in self.bot_list:
            bot.do_a_loop()


class balancer_bot(object):
    def __init__(self, qty, multiple, diff, init_price):
        self.status = 'running'
        self.run_time = 0
        self.qty = qty
        self.base = 0  # balanced stable asset
        self.multiple = multiple
        self.diff = diff
        self.buy_cnt = 0
        self.sell_cnt = 0

        # interface to get init price
        cur_price = init_price

        cur_val = self.qty * cur_price
        self.base = cur_val / (self.multiple) * (1.0 - self.multiple)
        logging.info(f"模拟平衡姬开单成功, 币数: {round(self.qty, 3)}, 价值: {round(cur_val, 3)}")
        logging.info(f"仓位比: {self.multiple}, 阈值: {self.diff}")

    def do_a_loop(self, t, cur_price):
        self.run_time = time


        logging.info(f"{self.asset} 模拟平衡姬正常运行中, 多次: {self.buy_cnt}, 空次: {self.sell_cnt}")
        if self.status != 'running':
            return -1
        cur_val = self.qty * cur_price
        val_to_d = (1.0 - self.multiple) * cur_val - self.multiple * self.base
        if abs(val_to_d) > 3.0 * self.diff:
            logging.info("平衡姬 " + self.asset + " 待平衡值过大 已暂停!")
            self.status = 'pause'
        if val_to_d > self.diff:
            self.qty -= val_to_d / cur_price
            self.base += val_to_d
            self.sell_cnt += 1
        elif val_to_d < -self.diff:
            self.qty += val_to_d / cur_price
            self.base -= val_to_d
            self.buy_cnt += 1



class grid_bot(object):
    def __init__(self, price_mode, price_diff, low, high, fund):
        self.run_time = 0

        self.low = low
        self.high = high
        self.fund = fund
        self.earn = 0

        self.price_mode = price_mode
        self.price_diff = price_diff

        self.orders = []

        logging.info('开始模拟,模式:{}'.format('现货U本位'))
        logging.info('区间:{}-{},总投资额:{}'.format(
            self.low, self.high, self.fund))

    def setup(self, price0):
        self.qty_each  = self.fund / price0 / (self.high - self.low) * self.price_diff

    def order(self, price, qty, direct):
        order = {'price': price, 'qty': qty, 'direct': direct}
        return order

    def do_a_loop(self, cur_price):
        self.orders.sort(key=lambda x: float(x['price']), reverse=False)  # 最高价到最低价.
        # {'price': price, 'qty': qty, 'direct': direct} direct:1-buy,0-sell
        for buy_order in self.buy_orders:
            if cur_price < buy_order['price']:

            if check_order:
                if check_order['status'] == 'CANCELED':
                    buy_delete_orders.append(buy_order)
                    # print(f"buy order status was canceled: {check_order.get('status')}")
                elif check_order['status'] == 'FILLED':
                    logging.info(
                        f"{self.symbol}买单成交,价格:{round(order_price, 3)}")
                    # logging.info(f"当前未成买单个数:{len(self.buy_orders)-1}")
                    # 买单成交，挂卖单.
                    if self.price_mode == 'arithmetic':
                        sell_price = order_price + self.price_diff
                    else:
                        sell_price = order_price * (1 + self.price_diff)

                    if 0 < sell_price < ask_price:
                        # 防止价格
                        sell_price = ask_price

                    params = order_str_limit(self.symbol, side='SELL', type='LIMIT', timeInForce='GTC',
                                             quantity=round_to((self.fund_each / sell_price), self.qty_unit),
                                             price=round_to(sell_price, self.price_unit))

                    new_sell_order_id = self.client.new_order(**params)

                    logging.info(f'{self.symbol}买单成交！挂卖单,价格:{round(sell_price, 3)}')

                    # 若挂单成功
                    if new_sell_order_id:
                        # 注意转换
                        new_sell_order = {'order_id': new_sell_order_id['orderId'], 'price': sell_price}
                        buy_delete_orders.append(buy_order)
                        self.sell_orders.append(new_sell_order)

                    # 最低价买单成交，下方挂新买单
                    if order_price <= self.order_min_price:
                        if (self.price_mode == 'arithmetic'):
                            buy_price = order_price - self.price_diff
                        else:
                            buy_price = order_price * (1 - self.price_diff)
                        if buy_price > bid_price > 0:
                            buy_price = bid_price

                        params = order_str_limit(self.symbol, side='BUY', type='LIMIT', timeInForce='GTC',
                                                 quantity=round_to((self.fund_each / buy_price), self.qty_unit),
                                                 price=round_to(buy_price, self.price_unit))
                        new_buy_order_id = self.client.new_order(**params)

                        logging.info(f'{self.symbol}最低买单成交！挂新最低买单,价格:{round(buy_price, 3)}')
                        self.order_min_price = buy_price
                        if new_buy_order_id:
                            # 注意转换
                            new_buy_order = {'order_id': new_buy_order_id['orderId'], 'price': buy_price}
                            self.buy_orders.append(new_buy_order)


        # 卖单逻辑, 检查卖单成交情况.
        for sell_order in self.sell_orders:

            check_order = self.client.get_order(self.symbol, orderId=sell_order['order_id'])
            order_price = sell_order['price']

            if check_order:
                if check_order['status'] == 'CANCELED':
                    # print(f"sell order status was canceled: {check_order.get('status')}")
                elif check_order['status'] == 'FILLED':
                    self.txn_count += 1
                    self.earned += (self.fund_each / (order_price)) - (self.fund_each / (order_price + self.price_diff))
                    logging.info(
                        f"{self.symbol}卖单成交,价格:{round(order_price, 3)},"
                        f"累计收益：{round(self.earned, 3)}")
                    # logging.info(f"当前未成卖单数:{len(self.sell_orders)-1}")
                    # 卖单成交，先下买单.
                    if (self.price_mode == 'arithmetic'):
                        buy_price = order_price - self.price_diff
                    else:
                        buy_price = order_price * (1 - self.price_diff)
                    if buy_price > bid_price > 0:
                        buy_price = bid_price

                    params = order_str_limit(self.symbol, side='BUY', type='LIMIT', timeInForce='GTC',
                                             quantity=round_to((self.fund_each / buy_price), self.qty_unit),
                                             price=round_to(buy_price, self.price_unit))
                    new_buy_order_id = self.client.new_order(**params)

                    logging.info(f'{self.symbol}卖单成交！挂买单,价格:{round(buy_price, 3)}')

                    if new_buy_order_id:
                        # 注意转换
                        new_buy_order = {'order_id': new_buy_order_id['orderId'], 'price': buy_price}
                        sell_delete_orders.append(sell_order)
                        self.buy_orders.append(new_buy_order)

                    # 最高卖单成交后在上方再挂卖单
                    if order_price >= self.order_max_price:
                        if (self.price_mode == 'arithmetic'):
                            sell_price = order_price + self.price_diff
                        else:
                            sell_price = order_price * (1 + self.price_diff)

                        if 0 < sell_price < ask_price:
                            # 防止价格
                            sell_price = ask_price

                        params = order_str_limit(self.symbol, side='SELL', type='LIMIT', timeInForce='GTC',
                                                 quantity=round_to((self.fund_each / sell_price), self.qty_unit),
                                                 price=round_to(sell_price, self.price_unit))
                        new_sell_order_id = self.client.new_order(**params)

                        logging.info(f'{self.symbol}最高卖单成交！挂新最高卖单,价格:{round(sell_price, 3)}')
                        self.order_max_price = sell_price

                        if new_sell_order_id:
                            # 注意转换
                            new_sell_order = {'order_id': new_sell_order_id['orderId'], 'price': sell_price}
                            self.sell_orders.append(new_sell_order)


