import tkinter

class AMM_calculator(object):
    def __init__(self, pa0, pb0,):
        self.pa0 = pa0
        self.pb0 = pb0

class GridCalculator(object):
    def __init__(self, fund_each):
        self.fund_each = fund_each
    def set_diff(self, diff):
        self.diff = diff
    def set_profit(self, profit):
        self.profit = profit
    def set_p0(self, p0):
        self.p0 = p0

    def get_diff(self):
        ans = self.p0 * self.p0 * self.profit / (self.fund_each - self.profit * self.profit)
        return ans


class ToolGui(object):
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    def set_init_window(self):
        self.init_window_name.title('Uya Parameter Calculator')
        self.init_window_name.geometry('1068x681+10+10')
        # 标签
        self.init_data_label = tkinter.Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = tkinter.Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = tkinter.Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)
        # 文本框
        self.init_data_Text = tkinter.Text(self.init_window_name, width=67, height=35)  # 原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = tkinter.Text(self.init_window_name, width=70, height=49)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = tkinter.Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        # 按钮
        self.str_trans_to_md5_button = tkinter.Button(self.init_window_name, text="字符串转MD5", bg="lightblue", width=10,
                                              command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=1, column=11)
        return 0


    def str_trans_to_md5(self):
            src = self.init_data_Text.get(1.0, tkinter.END).strip().replace("\n", "").encode()
            # print("src =",src)


            # 输出到界面
            self.result_data_Text.delete(1.0, tkinter.END)
            self.result_data_Text.insert(1.0, 1)

            self.write_log_to_Text("ERROR:str_trans_to_md5 failed")


        # 日志动态打印
    def write_log_to_Text(self, logmsg):
            global LOG_LINE_NUM
            current_time = self.get_current_time()
            logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
            if LOG_LINE_NUM <= 7:
                self.log_data_Text.insert(tkinter.END, logmsg_in)
                LOG_LINE_NUM = LOG_LINE_NUM + 1
            else:
                self.log_data_Text.delete(1.0, 2.0)
                self.log_data_Text.insert(tkinter.END, logmsg_in)







if __name__ == '__main__':
    t1 = GridCalculator(20)
    t1.set_profit(0.1)
    t1.set_p0(100)
    print(t1.get_diff())
    exit(0)

    init_window = tkinter.Tk() # 实例化出一个父窗口
    ZMJ_PORTAL = ToolGui(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


