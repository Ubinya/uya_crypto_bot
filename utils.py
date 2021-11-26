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


def order_str(symbol, side, type, timeInForce, quantity, price):
    params = {
        "symbol": symbol,
        "side": side,
        "type": type,
        "timeInForce": timeInForce,
        "quantity": quantity,
        "price": price,
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

