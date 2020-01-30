from __future__ import division
from pprint import pprint, pformat


class State:
    def __init__(self, name, u, v, m, p):
        self.name = name
        self.u = u
        self.v = v
        self.m = m
        self.p = p
        self.optimized = 'R_OPT'
        self.update_r()
        self.update_optimum()
        self.optimize('R_OPT')

    def optimize(self, text):
        if text == 'S_OPT' or text == 'R_OPT':
            self.optimized = text
            if self.optimized == 'S_OPT':
                self.f = self.optimum
            elif self.optimized == 'R_OPT':
                self.f = 1 - self.optimum

    def update_r(self):
        self.r = self.u / self.v

    def update_optimum(self):
        if self.v > 0:
            self.optimum = 1
        elif self.v < 0:
            self.optimum = 0

    def update_f(self, f):
        self.f = f
        if self.f == self.optimum:
            self.optimized = 'S_OPT'
        elif self.f == 1 - self.optimum:
            self.optimized = 'R_OPT'
        else:
            self.optimized = None

    def update_u(self, value):
        self.u = value
        self.update_r()


class Data:
    def __init__(self):
        self.r_utility = 0
        self.s_utility = 0
        self.m_utility = 0
        self.states = set()
        name = ['1', '2', '3', '4']
        u = [4, -8, 12, -16]
        v = [-12, 12, -12, 12]
        m = [4, -8, 12, -16]
        p = [.25, .25, .25, .25]
        for i in xrange(len(u)):
            state = State(name[i], u[i], v[i], m[i], p[i])
            self.states.add(state)
            # the prior is the better action utility given no information, the utility here (the delta) is negative
            # if self.update_utility() > 0:
            #     for state in self.states:
            #         state.u = state.u * (-1)

    def update_utilities(self):
        r_utility = 0
        s_utility = 0
        m_utility = 0
        for state in self.states:
            # multiply by probability if not uniform
            r_utility += state.p * state.f * state.u
            s_utility += state.p * state.f * state.v
            m_utility += state.p * state.f * state.m
        self.r_utility = r_utility
        self.s_utility = s_utility
        self.m_utility = m_utility
        return r_utility, s_utility, m_utility

    def print_state(self):
        states_list = sorted(self.states, key=lambda x: x.r, reverse=True)
        print '\n<CURRENT STATUS>'
        print '****************'
        text = 'name = '.ljust(15)
        for state in states_list:
            text += str(state.name).ljust(8)
        text += '\nu = '.ljust(15)
        for state in states_list:
            text += str(state.u).ljust(8)
        text += '\nv = '.ljust(15)
        for state in states_list:
            text += str(state.v).ljust(8)
        text += '\nr = '.ljust(15)
        for state in states_list:
            text += str(int(100 * state.r) / 100).ljust(8)
        text += '\np = '.ljust(15)
        for state in states_list:
            text += str(state.p).ljust(8)
        text += '\noptimum = '.ljust(15)
        for state in states_list:
            text += str(state.optimum).ljust(8)
        text += '\noptimized = '.ljust(15)
        for state in states_list:
            if state.optimized:
                text += str(state.optimized).ljust(8)
            else:
                text += 'w*'.ljust(8)
        text += '\nf = '.ljust(15)
        for state in states_list:
            text += str(int(100 * state.f) / 100).ljust(8)
        text += '\n%opt = '.ljust(15)
        for state in states_list:
            text += str(int(100 * (1 - state.optimum + (2 * state.optimum - 1) * state.f)) / 100).ljust(8)

        r_utility, s_utility, m_utility = self.update_utilities()
        text += '\nr_utility = '.ljust(15)
        text += str(r_utility)
        text += '\ns_utility = '.ljust(15)
        text += str(s_utility)
        text += '\nm_utility = '.ljust(15)
        text += str(m_utility)
        print text


    def optimize_one_state(self):
        print '\n<OPTIMIZING A STATE>'
        print '********************'
        selected = None
        for state in self.states:
            if not selected:
                if state.optimized == 'R_OPT':
                    print 'default exist, selected', state.name
                    selected = state
            if state.optimized == 'R_OPT' and state.r > selected.r:
                print 'changed to', state.name
                selected = state
        if selected:
            print 'optimizing', selected.name
            selected.optimize('S_OPT')
            return selected
        else:
            print 'nothing was selected - no R-OPT states?'


    def optimize_all(self):  # all states
        last = None
        delta_r_utility = None
        last_r_utility = None
        current_r_utility = self.update_utilities()[0]
        while current_r_utility > 0:
            last_r_utility = self.r_utility
            last = self.optimize_one_state()
            current_r_utility = self.update_utilities()[0]
            delta_r_utility = last_r_utility - current_r_utility
            # print last_r_utility, current_r_utility, delta_r_utility
            if current_r_utility > 0:
                print 'IC threshold not reached'
                self.print_state()
            else:
                print 'IC threshold reached'

        print 'calculating f(w*)'
        if last.optimum == 1:
            last.update_f(last_r_utility / delta_r_utility)
        elif last.optimum == 0:
            last.update_f(1 - last_r_utility / delta_r_utility)
        self.print_state()



if __name__ == "__main__":
    data = Data()
    data.print_state()
    data.optimize_all()
