import os
import sys
import requests
from pprint import pprint
import time
import logging
# import backtrader as bt
import numpy as np
from binance.spot import Spot as Client
from decimal import Decimal
import json
# from binance.lib.utils import config_logging
from binance.error import ClientError
from key import *
from utils import *


class balance_bot(object):
    def __init__(self, client, asset, symbol, multiple, diff):
        self.status = 'running'
        self.asset = asset
        self.symbol = symbol
        self.run_time = 0
        self.qty = 0
        self.base = 0 # balanced stable asset
        self.multiple = multiple
        self.diff = diff
        self.client = client
        self.buy_cnt = 0
        self.sell_cnt = 0

        trade_info = client.exchange_info(symbol=self.symbol)
        items = trade_info.get('symbols', [])

        self.price_unit = float(items[0]['filters'][0]['tickSize'])
        self.qty_unit = float(items[0]['filters'][2]['stepSize'])

        res = self.client.account()
        balance_list = res.get('balances', -1)
        for item in balance_list:
            if item.get('asset') == self.asset:
                self.qty = round_to(float(item.get('free')), self.qty_unit)
                break
        cur_price = float(self.client.ticker_price(self.symbol)['price'])
        cur_val = self.qty * cur_price
        self.base = cur_val / (self.multiple) * (1.0 - self.multiple)
        logging.info(f"{self.asset} 平衡姬开单成功, 当前价值: {round(cur_val, 3)}, 仓位比: {self.multiple}, 阈值: {self.diff}")


    def do_a_loop(self):
        self.run_time += 20

        with open((self.symbol+'.json'), 'w') as f:
            save = {'symbol': self.symbol, 'run_time': self.run_time,
                    'buy_cnt': self.buy_cnt, 'sell_cnt': self.sell_cnt}
            json_str = json.dumps(save)
            f.write(json_str)

        if self.run_time % 300 != 0:
            return 0
        if self.run_time % 3600 == 0:
            logging.info(f"{self.asset} 平衡姬正常运行中, 多次: {self.buy_cnt}, 空次: {self.sell_cnt}")
        if self.status != 'running':
            return -1
        cur_price = float(self.client.ticker_price(self.symbol)['price'])
        cur_val = self.qty * cur_price
        val_to_d = (1.0 - self.multiple) * cur_val - self.multiple * self.base
        if abs(val_to_d) > 3.0*self.diff:
            logging.info("平衡姬 "+self.asset+" 待平衡值过大 已暂停!")
            self.status = 'pause'
        if val_to_d > self.diff:
            logging.info(f'val={cur_val} 需要卖出{val_to_d}')
            res = self.trade('sell', val_to_d)
            self.qty -= round_to(float(res.get('executedQty')), self.qty_unit)
            self.base += round_to(float(res.get('cummulativeQuoteQty')), self.price_unit)
            self.sell_cnt += 1
        elif val_to_d < -self.diff:
            logging.info(f'val={cur_val} 需要卖出{val_to_d}')
            res = self.trade('buy', val_to_d)
            self.qty += round_to(float(res.get('executedQty')), self.qty_unit)
            self.base -= round_to(float(res.get('cummulativeQuoteQty')), self.price_unit)
            self.buy_cnt += 1


    def trade(self, direction, val_d):
        if direction == 'buy':

            params = order_str_market(self.symbol, side='BUY', type='MARKET',
                                    quoteOrderQty=round_to(val_d, self.price_unit))
        elif direction == 'sell':
            params = order_str_market(self.symbol, side='SELL', type='MARKET',
                                    quoteOrderQty=round_to(val_d, self.price_unit))
        else:
            return False

        return self.client.new_order(**params)

class grid_bot(object):
    def __init__(self, client, symbol, price_mode, price_diff, max_order, fund_each=-1):
        self.client = client
        self.txn_count = 0
        self.run_time = 0

        self.earned = 0
        self.fund_each = fund_each

        self.symbol = symbol
        self.max_order = max_order
        self.price_mode = price_mode
        self.price_diff = price_diff
        self.sell_trigger = 0 # max trigger num is 3

        self.order_max_price = 0.0
        self.order_min_price = 9999999.0

        self.last_prise_index = None
        self.upper = None
        self.lower = None

        self.buy_orders = []  # 买单.
        self.sell_orders = []  # 卖单.

        trade_info = client.exchange_info(symbol=self.symbol)
        items = trade_info.get('symbols', [])

        self.price_unit = float(items[0]['filters'][0]['tickSize'])
        self.qty_unit = float(items[0]['filters'][2]['stepSize'])

        logging.info('本分姬交易对:{},模式:{}'.format(
            self.symbol, '现货U本位'))
        logging.info('最大订单数:{},每格投资额:{}'.format(
            self.max_order, self.fund_each
        ))
        # logging.info('down:{},up:{},price_diff:{}'.format(down,up,self.price_diff))


    def get_bid_ask_price(self):
        ticker = self.client.book_ticker(self.symbol)
        bid_price = 0
        ask_price = 0
        if ticker:
            bid_price = float(ticker['bidPrice'])
            ask_price = float(ticker['askPrice'])

        return bid_price, ask_price

    def make_limit_order(self, direction, ):


    def do_a_loop(self):
        self.run_time += 20

        rdata = self.client.ticker_price(self.symbol)
        price_cur = float(rdata['price'])

        if self.run_time % 3600 == 0:
            logging.info('本分姬交易对:{},运行时间:{}s,当前价格:{}'.format(
                self.symbol, self.run_time, round(price_cur, 3)))

        with open((self.symbol+'.json'), 'w') as f:
            save = {'symbol': self.symbol, 'run_time': self.run_time,
                    'txn': self.txn_count, 'earned': self.earned}
            json_str = json.dumps(save)
            f.write(json_str)

        bid_price, ask_price = self.get_bid_ask_price()
        # print(f"bid_price: {bid_price}, ask_price: {ask_price}")

        self.buy_orders.sort(key=lambda x: float(x['price']), reverse=True)  # 最高价到最低价.
        self.sell_orders.sort(key=lambda x: float(x['price']), reverse=False)  # 最低价到最高价.
        # print(f"buy orders: {self.buy_orders}")
        # print("------------------------------")
        # print(f"sell orders: {self.sell_orders}")

        buy_delete_orders = []  # 需要删除买单
        sell_delete_orders = []  # 需要删除的卖单

        # 买单逻辑,检查成交的情况.
        # {'oder_id':str,'price':float}
        # price只有在place_order时转换为str并只保留两位，其余任一时候是float
        for buy_order in self.buy_orders:

            check_order = self.client.get_order(self.symbol, orderId=buy_order['order_id'])
            order_price = buy_order['price']

            if check_order:
                if check_order['status'] == 'CANCELED':
                    buy_delete_orders.append(buy_order)
                    # print(f"buy order status was canceled: {check_order.get('status')}")
                elif check_order['status'] == 'NEW': # 不记得这是不是‘NEW’
                    break
                elif check_order['status'] == 'FILLED':
                    self.sell_trigger += 1
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

        # 过期或者拒绝的订单删除掉.
        for delete_order in buy_delete_orders:
            self.buy_orders.remove(delete_order)


        # 卖单逻辑, 检查卖单成交情况.
        for sell_order in self.sell_orders:

            check_order = self.client.get_order(self.symbol, orderId=sell_order['order_id'])
            order_price = sell_order['price']

            if check_order:
                if check_order['status'] == 'CANCELED':
                    sell_delete_orders.append(sell_order)
                    # print(f"sell order status was canceled: {check_order.get('status')}")
                elif check_order['status'] == 'NEW':  # 不记得这是不是‘NEW’
                    break
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
                        buy_price = order_price *(1- self.price_diff)
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

                    if self.sell_trigger < 4 :
                        # 最高卖单成交后在上方再挂卖单
                        if order_price >= self.order_max_price:
                            if (self.price_mode == 'arithmetic'):
                                sell_price = order_price + self.price_diff
                            else:
                                sell_price = order_price * (1 + self.price_diff)

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
                    else:
                        logging.info("警告！已经连卖3格, 已经暂停新单")



        # 过期或者拒绝的订单删除掉.
        for delete_order in sell_delete_orders:
            self.sell_orders.remove(delete_order)

        # 没有买单的时候.
        if len(self.buy_orders) <= 0:

            if bid_price > 0:
                if (self.price_mode == 'arithmetic'):
                    price = bid_price - self.price_diff
                else:
                    price = bid_price *(1- self.price_diff)

                params = order_str_limit(self.symbol, side='BUY', type='LIMIT', timeInForce='GTC',
                                   quantity=round_to((self.fund_each / price), self.qty_unit),
                                   price=round_to(price, self.price_unit))

                buy_order_id = self.client.new_order(**params)

                self.order_min_price = price
                if buy_order_id:
                    # 注意转换
                    buy_order = {'order_id': buy_order_id['orderId'], 'price': price}
                    self.buy_orders.append(buy_order)
                    logging.info(f'{self.symbol}没有买单！挂一个！价格：{round_to(price, self.price_unit)}')

        elif len(self.buy_orders) > int(self.max_order):  # 最多允许的挂单数量.
            # 订单数量比较多的时候.
            self.buy_orders.sort(key=lambda x: float(x['price']), reverse=False)  # 最低价到最高价

            delete_order = self.buy_orders[0]
            order = self.client.cancel_order(self.symbol, orderId=delete_order['order_id'])
            if order:
                self.buy_orders.remove(delete_order)

        # 没有卖单的时候.
        if len(self.sell_orders) <= 0:
            if ask_price > 0:
                if (self.price_mode == 'arithmetic'):
                    price = ask_price + self.price_diff
                else:
                    price = ask_price * (1+ self.price_diff)

                params = order_str_limit(self.symbol, side='SELL', type='LIMIT', timeInForce='GTC',
                                   quantity=round_to((self.fund_each / price), self.qty_unit),
                                   price=round_to(price, self.price_unit))
                sell_order_id = self.client.new_order(**params)

                self.order_max_price = price
                if sell_order_id:
                    # 注意转换
                    sell_order = {'order_id': sell_order_id['orderId'], 'price': price}
                    self.sell_orders.append(sell_order)
                    logging.info(f'{self.symbol}没有卖单！挂一个！价格：{round_to(price, self.price_unit)}')

        elif len(self.sell_orders) > int(self.max_order):  # 最多允许的挂单数量.
            # 订单数量比较多的时候.
            self.sell_orders.sort(key=lambda x: x['price'], reverse=True)  # 最高价到最低价

            delete_order = self.sell_orders[0]
            order = self.client.cancel_order(self.symbol, orderId=delete_order['order_id'])
            if order:
                self.sell_orders.remove(delete_order)