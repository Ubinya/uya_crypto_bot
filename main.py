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
from key import *
from utils import *
from module import bots

log_format = '%(asctime)s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
    format=log_format, datefmt='%m/%d %I:%M:%S %p')
fh = logging.FileHandler('log.txt')
fh.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(fh)

def _get_server_time():
    return int(time.time())



class BotManager(object):
    def __init__(self):
        logging.info('给狗修金大人请安~这里是量化姬,准备开始本次调教(调试)了!!')
        self.bot_list = []
        self.client = Client(key, secret, base_url=url)

    def add_grid_bot(self, symbol, price_mode, price_diff, max_order, fund_each):
        insbot = bots.grid_bot(self.client, symbol, price_mode, price_diff, max_order, fund_each)
        self.bot_list.append(insbot)


    def add_balance_bot(self, asset, symbol, multiple, diff):
        insbot = bots.balance_bot(self.client, asset, symbol, multiple, diff)
        self.bot_list.append(insbot)


    def run_init(self):
        self.bot_num = len(self.bot_list)
        logging.info("交易分姬数:{}".format(self.bot_num))

    def do_manager_loop(self):
        with open('BotManager.json', 'w') as f:
            save = {'status': "running", 'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), }
            json_str = json.dumps(save)
            f.write(json_str)
        for bot in self.bot_list:
            bot.do_a_loop()



if __name__ == '__main__':
    bot_manager = BotManager()
    # 交易对，价差模式：等差/等比，价差数额，最大订单数，每格金额
    bot_manager.add_grid_bot(symbol='BNBBUSD', price_mode='geometric', price_diff=0.015, max_order=20, fund_each=20)
    bot_manager.add_grid_bot(symbol='AVAXBUSD', price_mode='geometric', price_diff=0.04, max_order=20, fund_each=20)
    # bot_manager.add_grid_bot(symbol='GTCBUSD', price_mode='geometric', price_diff=0.055, max_order=20, fund_each=20)

    bot_manager.run_init()
    last_err_time = 0.0
    re_err_cnt = 0

    while True:
        try:
            bot_manager.do_manager_loop()
            time.sleep(20)

        except Exception as error:
            this_err_time = time.time()
            if this_err_time - last_err_time <= 10.0:
                re_err_cnt += 1
            else:
                re_err_cnt = 1
            if re_err_cnt == 3:
                logging.info("警告！发生严重错误！！请检查交易姬后台")
                with open('BotManager.json', 'w') as f:
                    save = {'status': "error", 'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                            'error': str(error.error_message)}
                    json_str = json.dumps(save)
                    f.write(json_str)
                exit()
            logging.info(f"catch error:{error}")
            last_err_time = this_err_time

            time.sleep(5)


