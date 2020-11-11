import math
import random
from matplotlib import pyplot as plt

class Grid:

    def __init__(self):
        self.vpps = []
        self.pib = 1000
        self.min_pib = 9999999
        self.max_pib = 0
        self.sum_pay = 0
        self.time_error = 0

    def add_vpp(self, vpp_boss):
        self.vpps.append(vpp_boss)

    def remove_vpp(self, vpp_boss):
        self.vpps.remove(vpp_boss)

    def pib_coef(self, out):
        # for fixed price uncomment
        # return 6.5
        if out > 1:
            return math.log(out)
        else:
            return 0

    def count_pay(self, out, acc_scr):
        pay = out * self.pib_coef(out) * self.pib * acc_scr
        return pay

    def calc_mse_error(self, error_list):
        mse = 0
        for item in error_list:
            mse += item * item
        # print(mse)
        return mse / len(error_list)

    def sort_by_len(self, vpp):
        return len(vpp.childs)

    def pay_for_time(self, time):
        self.min_pib = 99999999
        self.max_pib = 0
        self.sum_pay = 0
        errors = []
        for vpp in self.vpps:
            method = "mse"
            out = vpp.output_sum(time)
            # forec = vpp.forecast_sum(time)
            acc_scr = vpp.acc_score(time, True, method)
            pay = self.count_pay(out, acc_scr)
            self.min_pib = min(self.min_pib, self.pib_coef(out))
            self.max_pib = max(self.max_pib, self.pib_coef(out))
            self.sum_pay += pay
            vpp.get_paid(pay, time, self.pib_coef(out), method)
           # errors.append(vpp.calc_holon_error(time))
           #  if len(vpp.childs) > 3 or len(errors) == 0:

            for i in range(len(vpp.childs) + 1):
                errors.append((vpp.output_sum(time) - vpp.forecast_sum(time)) / (len(vpp.childs) + 1))

        # self.vpps.sort(key = self.sort_by_len)
        # for i in range(-1, -5, -1):
        #     print(i, len(vpp.childs))
        #     vpp = self.vpps[i]
        #     #for i in range(len(vpp.childs) + 1):
        #     errors.append((vpp.output_sum(time) - vpp.forecast_sum(time)) / (len(vpp.childs) + 1))

        self.sum_pay /= 175 # number of agents
        if len(errors):
            self.time_error = self.calc_mse_error(errors)
        else:
            self.time_error = 25000

    def negotiate(self, time):
        num_of_vpps = len(self.vpps)
        req_per_hour = int(num_of_vpps/24 + 1)
        start = (time % 24) * req_per_hour
        for i in range(start, start + req_per_hour):
            vpp = self.vpps[i % len(self.vpps)]
            for j in range(5):
                random_holon = random.randint(0, len(self.vpps) - 1)
                if random_holon == i % len(self.vpps):
                    continue
                else:
                    vpp2 = self.vpps[random_holon]
                    if vpp.negotiate(vpp2):
                        self.vpps.remove(vpp)
                        break

    def check_for_satisfaction(self):
        for vpp in self.vpps:
            vpp.check_for_satisfaction(self)

    def log_report(self, time):
        # print(f"Number of vpps: {len(self.vpps)}")
        # print(f"Average of max and min : {(self.max_pib + self.min_pib)/2}")
        # print(f"Sum pay: {self.sum_pay}")
        self.history['nov'].append(175.0 / len(self.vpps))
        self.history['aomm'].append((self.max_pib + self.min_pib)/2)
        self.history['sp'].append(self.sum_pay)
        self.history['error'].append(self.time_error)
        if (time + 1) % 24 == 0:
            avg = 0
            for i in range(-1, -25, -1):
                avg += self.history['sp'][i]
            avg /= 24
            self.history['spday'].append(avg)

        if (time + 1) % 24 == 0:
            avg = 0
            for i in range(-1, -25, -1):
                avg += self.history['error'][i]
            avg /= 24
            self.history['errorday'].append(avg)

    def show_report(self):
        print(len(self.history['spday']))
        print(self.history['nov'][-10:])
        plt.plot(self.history['sp'])
        plt.show()
        plt.plot(self.history['spday'])
        plt.show()
        # plt.plot(self.history['nov'])
        # plt.show()
        plt.plot(self.history['errorday'])
        plt.show()
    def run(self):
        frames = 744
        self.history = {}
        self.history['nov'] = []
        self.history['aomm'] = []
        self.history['sp'] = []
        self.history['spday'] = []
        self.history['error'] = []
        self.history['errorday'] = []
        for time in range(744):
            self.pay_for_time(time)
            self.negotiate(time)
            self.check_for_satisfaction()
            self.log_report(time)
        #self.show_report()
        return self.history
