from __future__ import division
from pprint import pprint, pformat

class State:
    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.optimized = "NO"
        self.update_r()
        self.update_optimum()
        self.optimize('NO')

    def optimize(self, text):
        if text == "OPT" or text == "NO":
            self.optimized = text
            if self.optimized == "OPT":
                self.f = self.optimum
            elif self.optimized == "NO":
                self.f = 1 - self.optimum

    def update_r(self):
        self.r = self.u/self.v

    def update_optimum(self):
        if self.v > 0:
            self.optimum = 1
        elif self.v < 0:
            self.optimum = 0

    def update_f(self, f):
        self.f = f
        if self.f == self.optimum:
            self.optimized = "OPT"
        elif self.f == 1 - self.optimum:
            self.optimized = "NO"
        else:
            self.optimized = None


    def update_u(self, value):
        self.u = value
        self.update_r


class Data:
    def __init__(self):
        self.states = set()
        us = [1, -2, 3, -4]
        vs = [-1, 1, -1, 1]
        for i in xrange(len(us)):
            state = State(us[i], vs[i])
            self.states.add(state)
        # the prior is the better action utility given no information, the utility here (the delta) is negative
        # if self.update_utility() > 0:
        #     for state in self.states:
        #         state.u = state.u * (-1)

    def update_utilities(self):
        r_utility = 0
	s_utility = 0
        for state in self.states:
            r_utility += state.f * state.u
            s_utility += state.f * state.v
        self.r_utility = r_utility
        self.s_utility = s_utility
        return r_utility, s_utility

    def print_state(self):
        states_list = sorted(self.states, key=lambda x: x.r, reverse=True)
        text = '**************************************************'
        text += '\nu = '.ljust(15)
        for state in states_list:
            text += str(state.u).ljust(8)
        text += '\nv = '.ljust(15)
        for state in states_list:
            text += str(state.v).ljust(8)
        text += '\nr = '.ljust(15)
        for state in states_list:
            text += str(int(100*state.r)/100).ljust(8)
        text += '\noptimum = '.ljust(15)
        for state in states_list:
            text += str(state.optimum).ljust(8)
        text += '\noptimized = '.ljust(15)
        for state in states_list:
            text += str(state.optimized).ljust(8)
        text += '\nf = '.ljust(15)
        for state in states_list:
            text += str(int(100*state.f)/100).ljust(8)
	r_utility, s_utility = self.update_utilities()
        text += '\nr_utility = '.ljust(15)
        text += str(r_utility)
        text += '\ns_utility = '.ljust(15)
        text += str(s_utility)
        print text


    def optimize_one_state(self):
        selected = None
        for state in self.states:
            if not selected:
                selected = state
            if state.optimized == 'NO' and state.r > selected.r:
                selected = state
        if selected:
            selected.optimize('OPT')
            return selected

    def optimize_all(self): # all states
        last = None
        current_utility = self.update_utilities()[0]
        while current_utility >=0:
            last_utility = self.r_utility
            last = self.optimize_one_state()
            current_utility = self.update_utilities()[0]
            delta_utility = last_utility - current_utility
            if current_utility >= 0:
                self.print_state()

        if last.optimum == 1:
            last.update_f(last_utility / delta_utility)
        elif last.optimum == 0:
            last.update_f(1 - last_utility / delta_utility)
        self.print_state()


if __name__ == "__main__":
    data = Data()
    data.print_state()
    data.optimize_all()

