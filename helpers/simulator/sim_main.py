import numpy as np
from time import time
from helpers.simulator.sim_bots import *
import math
import os
import matplotlib.pyplot as plt

class MarketGenerator(object):
    def __init__(self):
        self.market_path = "helpers/simulator/market_sim"
        self.s0 = None
        self.miu = None
        self.sigma = None
        self.tick_num = None

    def set_prams(self, s0, mean, sigma, tick_num):
        if s0 is not None: self.s0 = s0
        if mean is not None: self.mean = mean
        if sigma is not None: self.sigma = sigma
        if tick_num is not None: self.tick_num = tick_num

    def generate(self):
        dt = 1.0 / self.tick_num
        s1 = self.s0 * np.exp(self.mean * dt +
                    self.sigma * np.sqrt(dt) *
                    np.random.standard_normal(10000))
        return s1

    def show_market(self):
        dt = 1.0 / self.tick_num
        m = 10 # target num
        s = np.zeros((self.tick_num+1, m))
        s[0] = self.s0
        for t in range(1, self.tick_num+1):
            s[t] = s[t-1]* np.exp(self.mean * dt +
                    self.sigma * np.sqrt(dt) *
                    np.random.standard_normal(m))
        plt.plot(s[:,:], lw=1.5)
        plt.xlabel('time')
        plt.ylabel('price')
        plt.title('market simulation')
        plt.show()



def simulate():
    app = MarketGenerator()
    app.set_prams(s0=3100, mean=0, sigma=0.3, tick_num=300)
    app.show_market()
    exit()

    bot_manager = BotManager()
    # 交易对，价差模式：等差/等比，价差数额，最大订单数，每格金额
    # bot_manager.add_grid_bot(symbol='BNBBUSD', price_mode='geometric', price_diff=0.01, max_order=40, fund_each=20)
    bot_manager.add_balance_bot(asset='AVAX', symbol='AVAXBUSD', multiple=0.35, diff=11)

    bot_manager.run_init()
    last_err_time = 0.0
    re_err_cnt = 0

