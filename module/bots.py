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

log_format = '%(asctime)s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
    format=log_format, datefmt='%m/%d %I:%M:%S %p')
fh = logging.FileHandler('log.txt')
fh.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(fh)


class balancer_bot(object):
    def __init__(self, asset, symbol, multiple, diff, client):
        self.status = 'running'
        self.asset = asset
        self.symbol = symbol
        self.runtime = 0
        self.val = 0
        self.multiple = multiple
        self.diff = diff
        self.client = client
        self.buy_cnt = 0
        self.sell_cnt = 0

        trade_info = client.exchange_info(symbol=self.symbol)
        items = trade_info.get('symbols', [])

        self.price_unit = float(items[0]['filters'][0]['tickSize'])
        self.qty_unit = float(items[0]['filters'][2]['stepSize'])


    def do_a_loop(self):
        if self.status != 'running':
            return -1
        res = self.client.funding_wallet(asset=self.asset)
        cur_val = float(res[0].get('free', -1))
        val_d = cur_val - self.val
        if abs(val_d) > 4.0*self.diff:
            logging.info("平衡姬 "+self.asset+" 出现待平衡值过大 已暂停!")
            self.status = 'pause'
        if val_d > self.diff:
            self.trade('sell', val_d)
            self.sell_cnt += 1
        elif val_d < -self.diff:
            self.trade('buy', val_d)
            self.buy_cnt += 1







    def trade(self, direction, val_d):
        if direction == 'buy':
            # 麻了oder_str要重写一下
            params = self.order_str_market(self.symbol, side='BUY', type='MARKET', timeInForce='GTC',
                                    quoteOrderQty=round_to(val_d, self.qty_unit))
        else:
            params = self.order_str_market(self.symbol, side='SELL', type='MARKET', timeInForce='GTC',
                                    quoteOrderQty=round_to(val_d, self.qty_unit))

        order_res = self.client.new_order(**params)
