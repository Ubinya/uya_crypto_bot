import numpy as np
from time import time
from sim_bots import *
import matplotlib.pyplot as plt

class market_generator(object):
    def __init__(self, market_num, init_price ):
        S_0 = 100.0  # 股票或指数初始的价格;
        K = 105  # 行权价格
        T = 1.0  # 期权的到期年限(距离到期日时间间隔)
        r = 0.05  # 无风险利率
        sigma = 0.2  # 波动率(收益标准差)
        M = 50  # number of time steps
        dt = T / M  # time enterval
        I = 20000  # number of simulation
        # 20000条模拟路径，每条路径５０个时间步数
        S = np.zeros((M + 1, I))
        S[0] = S_0
        np.random.seed(2000)
        start = time()
        for t in range(1, M + 1):
        z = np.random.standard_normal(I)
        S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)

        C_0 = np.exp(-r * T) * np.sum(np.maximum(S[-1] - K, 0)) / I

        end = time()

        # 估值结果

        print('total time is %.6f seconds' % (end - start))

        print('European Option Value %.6f' % C_0)


        # 前２０条模拟路径


        plt.figure(figsize=(10, 7))

        plt.grid(True)

        plt.xlabel('Time step')

        plt.ylabel('index level')

        for i in range(20):
            plt.plot(S.T[i])


if __name__ == '__main__':
    bot_manager = BotManager()
    # 交易对，价差模式：等差/等比，价差数额，最大订单数，每格金额
    # bot_manager.add_grid_bot(symbol='BNBBUSD', price_mode='geometric', price_diff=0.01, max_order=40, fund_each=20)
    bot_manager.add_balance_bot(asset='AVAX', symbol='AVAXBUSD', multiple=0.35, diff=11)

    bot_manager.run_init()
    last_err_time = 0.0
    re_err_cnt = 0