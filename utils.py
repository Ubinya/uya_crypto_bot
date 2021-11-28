# -*- coding: UTF-8 -*-
import os
import sys
import requests
from pprint import pprint
import time
import logging
import numpy as np
from binance.spot import Spot as Client
from decimal import Decimal
import json
from binance.error import ClientError

log_format = '%(asctime)s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
    format=log_format, datefmt='%m/%d %I:%M:%S %p')
fh = logging.FileHandler('log.txt')
fh.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(fh)


def order_str_limit(symbol, side, type, timeInForce, quantity, price):
    params = {
        "symbol": symbol,
        "side": side,
        "type": type,
        "timeInForce": timeInForce,
        "quantity": quantity,
        "price": price,
    }
    return params

def order_str_market(symbol, side, type, timeInForce, quoteOrderQty):
    params = {
        "symbol": symbol,
        "side": side,
        "type": type,
        "timeInForce": timeInForce,
        "quoteOrderQty": quoteOrderQty,
    }
    return params

def round_to(value: float, target: float) -> float:
    """
    Round price to price tick value.
    """
    value = Decimal(str(value))
    target = Decimal(str(target))
    rounded = float(int(round(value / target)) * target)
    return rounded

