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

class balancer_bot(object):
    def __init__(self, val, multiple, diff, qty_unit, price_unit, client):
        self.runtime = 0
        self.val = val
        self.multiple = multiple
        self.diff = diff
        self.qty_unit = qty_unit
        self.price_unit = price_unit
        self.client = client

    def get_bid_ask_price(self):
        ticker = self.client.book_ticker(self.symbol)
        bid_price = 0
        ask_price = 0
        if ticker:
            bid_price = float(ticker['bidPrice'])
            ask_price = float(ticker['askPrice'])

        return bid_price, ask_price

    def do_a_loop(self):





    def trade(self, direction, d_val):
        if direction == 'buy':
            params = self.order_str(self.symbol, side='SELL', type='LIMIT', timeInForce='GTC',
                                    quantity=round_to((self.fund_each / buy_price), self.qty_unit),
                                    price=round_to(bur_price, self.price_unit))
        else:
            params = self.order_str(self.symbol, side='SELL', type='LIMIT', timeInForce='GTC',
                                    quantity=round_to((self.fund_each / sell_price), self.qty_unit),
                                    price=round_to(sell_price, self.price_unit))

        order_res = self.client.new_order(**params)
