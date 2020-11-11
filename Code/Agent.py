import math
import random
from matplotlib import pyplot as plt
import bisect

class Agent:
    initial = 0
    merge_threshold = 0.1
    def __init__(self, name, ftype):
        self.name = name
        self.ftype = ftype
        self.holon = Agent.initial
        Agent.initial += 1
        self.is_boss = True
        self.boss = self
        self.childs = []
        self.holon_errors_sorted = []
        self.holon_mse_sum = 0

        self.outs = []
        self.forecasts = []
        self.capacities = []
        self.errors_sorted = []
        self.mse_sum = 0

        self.incomes = []
        self.income_history = 0 # only for bosses
        self.alpha = 0.8
        self.pib_coef = 0
        self.acc_scr = 1
        self.mse_scr = 1

    def add_out(self, out):
        self.outs.append(int(out))

    def add_forec(self, forec):
        self.forecasts.append(int(forec))

    def add_capac(self, capac):
        self.capacities.append(int(capac))

    def calc_error(self, time):
        if self.forecast(time) == 0:
            return 0
        error = (self.output(time) - self.forecast(time)) / self.forecast(time)
        return error

    def calc_holon_error(self, time):
        if self.forecast_sum(time) == 0:
            return 0
        h_error = (self.output_sum(time) - self.forecast_sum(time)) / self.forecast_sum(time)
        return h_error

    def remove_childs(self):
        self.childs = []

    def remove_child(self, child):
        self.childs.remove(child)

    def remove_holon_errors(self):
        self.holon_errors_sorted = []

    def clear_income_history(self):
        self.income_history = 0

    def clear_holon_mse(self):
        self.holon_mse_sum = 0

    def merge_holon(self, h_boss):
        #if merge_con():
        h_boss.is_boss = False
        h_boss.boss = self
        for child in h_boss.childs:
            child.boss = self
            self.childs.append(child)
        h_boss.remove_childs()
        h_boss.clear_income_history()
        self.childs.append(h_boss)
        # for error in h_boss.holon_errors_sorted:    # ????????
        #     self.holon_errors_sorted.append(error)
        # self.holon_errors_sorted.sort()
        h_boss.remove_holon_errors()
        h_boss.clear_holon_mse()


    def check_merge_request(self, h_boss):
        if h_boss.income_history > Agent.merge_threshold * self.income_history: # if it is efficient to merge
            self.merge_holon(h_boss)
            return True
        else:
            return False

    def output(self, time):
        return self.outs[time]

    def forecast(self, time):
        return self.forecasts[time]

    def output_sum(self, time):
        output = 0
        for child in self.childs:
            output += child.output(time)
        output += self.output(time)
        return output

    def out_acc_sum(self, time, method):
        out_acc = 0
        for child in self.childs:
            out_acc += child.output(time) * child.acc_score(time, False, method)
        out_acc += self.output(time) * self.acc_score(time, False, method)
        return out_acc


    def forecast_sum(self, time):
        forecast = 0
        for child in self.childs:
            forecast += child.forecast(time)
        forecast += self.forecast(time)
        return forecast

    def get_paid(self, money, time, pib_coef, method):
        out_acc_sum = self.out_acc_sum(time, method)
        if out_acc_sum == 0:
            out_acc_sum = 1
        if self.is_boss:
            self.income_history = self.alpha * self.income_history + (1 - self.alpha) * money
            for child in self.childs:
                # out = child.output(time)
                # share = money * out / out_sum
                out_acc = child.output(time) * child.acc_scr
                share = money * out_acc / (out_acc_sum - out_acc + child.output(time))
                child.get_paid(share, time, pib_coef, method)
            # share = money * self.output(time) / out_sum
            out_acc = self.output(time) * self.acc_scr
            share = money * out_acc / (out_acc_sum - out_acc + self.output(time))
            self.incomes.append(share)
            # print(self.name, share)
            self.pib_coef = pib_coef
        else:
            self.incomes.append(money)
            # print(self.name, money)
            self.pib_coef = pib_coef

    def report_crps(self, errors_list, x):
        # x = self.calc_holon_error(time)
        N = len(errors_list)
        x_pos = bisect.bisect(errors_list, x)
        crps = 0

        for k in range(x_pos - 1):
            diff = errors_list[k + 1] - errors_list[k]
            crps += diff * ((k + 1) / N) * ((k + 1) / N)

        if x_pos > 0:
            diff = x - errors_list[x_pos - 1]
            crps += diff * ((x_pos + 1) / N) * ((x_pos + 1) / N)

        if x_pos < N:
            diff = errors_list[x_pos] - x
            crps += diff * (1 - (x_pos + 1) / N) * (1 - (x_pos + 1) / N)

        for k in range(x_pos, N - 1):
            diff = errors_list[k + 1] - errors_list[k]
            crps += diff * (1 - (k + 1) / N) * (1 - (k + 1) / N)

        crps = -1 * crps
        bisect.insort(errors_list, x)
        return crps

    def crps(self, time, calc_for_holon):
        if calc_for_holon:
            crps = self.report_crps(self.holon_errors_sorted, self.calc_holon_error(time))
        else:
            crps = self.report_crps(self.errors_sorted, self.calc_error(time))
        return crps

    def mse(self, time, calc_for_holon):
        if calc_for_holon:
            self.holon_mse_sum += self.calc_holon_error(time) * self.calc_holon_error(time)
            return self.holon_mse_sum
        else:
            self.mse_sum += self.calc_error(time) * self.calc_error(time)
            return self.mse_sum

    def acc_score(self, time, calc_for_holon, method):
        if method == "crps":
            crps = self.crps(time, calc_for_holon)
            if not calc_for_holon:
                self.acc_scr = 1 / (1 - crps)
            return 1 / (1 - crps)
        elif method == "mse":
            mse = self.mse(time, calc_for_holon)
            if not calc_for_holon:
                self.acc_scr = mse / (time + 1)
                self.acc_scr = 1 / math.exp(self.acc_scr)
            temp = mse / (time + 1)
            return 1 / math.exp(temp)
        elif method == "none":
            if not calc_for_holon:
                self.acc_scr = 1
            return 1

    def negotiate(self, h_boss):
        if self.income_history < h_boss.income_history:
            return h_boss.check_merge_request(self)
        else:
            return False

    def check_for_satisfaction(self, grid):
        if self.is_boss:
            for child in self.childs:
                child.check_for_satisfaction(grid)
        else:
            if self.pib_coef < (grid.min_pib + grid.max_pib)/2:
                self.boss.remove_child(self)
                self.is_boss = True
                self.boss = self
                grid.add_vpp(self)



