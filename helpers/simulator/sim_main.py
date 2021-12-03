import numpy as np
from time import time
from sim_bots import *
import matplotlib.pyplot as plt

class market_generator(object):
    def __init__(self, market_num, init_price ):
        return 0


if __name__ == '__main__':
    bot_manager = BotManager()
    # 交易对，价差模式：等差/等比，价差数额，最大订单数，每格金额
    # bot_manager.add_grid_bot(symbol='BNBBUSD', price_mode='geometric', price_diff=0.01, max_order=40, fund_each=20)
    bot_manager.add_balance_bot(asset='AVAX', symbol='AVAXBUSD', multiple=0.35, diff=11)

    bot_manager.run_init()
    last_err_time = 0.0
    re_err_cnt = 0