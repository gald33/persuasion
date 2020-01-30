from __future__ import division
from pprint import pprint, pformat
import random
from copy import deepcopy

show_opt_steps = False


class State:
    def __init__(self, name, u, v, m, p):
        self.name = name
        self.trans_u = u
        self.u = []
        self.v = v
        self.m = m
        self.p = p
        self.c = self.m / self.v
        self.optimized = None    #to make sure it exists
        self.reset_optimization()
        # self.trans_f = 1 - self.optimum # done (including A states) through reset_optimization()
        self.f = []

    def reset_optimization(self):   # and save last state stats
        self.update_r()
        self.update_optimum()
        if self.r >= 0:
            self.update_f(self.optimum)
        else:
            self.update_f(1 - self.optimum)

    # def optimize(self, text):
    #     if text == 'S_OPT' or text == 'R_OPT':
    #         self.optimized = text
    #         if self.optimized == 'S_OPT':
    #             self.f = self.optimum
    #         elif self.optimized == 'R_OPT':
    #             self.f = 1 - self.optimum

    def update_r(self):
        self.r = self.trans_u / self.v

    def update_optimum(self):
        if self.v > 0:
            self.optimum = 1
        elif self.v < 0:
            self.optimum = 0

    def update_f(self, f):
        self.trans_f = f
        if self.trans_f == self.optimum:
            if self.r >= 0:
                self.optimized = 'A'
            else:
                self.optimized = 'S_OPT'
        elif self.trans_f == 1 - self.optimum:
            self.optimized = 'R_OPT'
        else:
            self.optimized = 'w*'

    def update_u(self, value):
        self.trans_u = value
        self.update_r()


class Data:
    def __init__(self):
        self.r_utility = 0
        self.s_utility = 0
        self.m_utility = 0
        self.states = set()
        u = [4,  -0.001]
        v = [-1,  -1]
        m = [-4,   1]
        # u = [4,  -0.001,  1]
        # v = [-1,  -1,  -10]
        # m = [-4,   -80, -100]
        wanted_num_of_states = len(u)
        #wanted_num_of_states = 5
        name = xrange(1,wanted_num_of_states + 1)
        # m = random.sample(xrange(1,31), wanted_num_of_states)
        # pprint(m)
        # v = random.sample(xrange(1,31), wanted_num_of_states)
        # pprint(v)
        self.num_of_states = len(m)
        # p = [.25,.25,.5]
        p = [1/self.num_of_states] * self.num_of_states
        # pprint(p)
        for i in xrange(self.num_of_states):
            # m_sign = random.choice((-1,1))
            # print m_sign
            # state = State(name[i], m_sign * m[i], -m_sign * v[i], m_sign * m[i], p[i])
            state = State(name=name[i], u=u[i], v=v[i], m=m[i], p=p[i])
            # pprint(state)
            self.states.add(state)
            # the prior is the better action utility given no information, the utility here (the delta) is negative
            # if self.update_utility() > 0:
            #     for state in self.states:
            #         state.u = state.u * (-1)

    def style(self, text, styles, selected_state, state):
        if styles:
            # print 'before:' + pformat(styles)
            if not isinstance(styles, list):
                styles = [styles,]
        if isinstance(text, list):
            if len(text) > 1:    # compare two values
                # print 'save counter:', state.save_counter
                # pprint(text)
                # print str(type(text[0])),str(type(text[1]))
                if text[-1] > text[-2]:
                    # pprint(text)
                    styles.append('green')
                    # styles.append('green')
                elif text[-1] < text[-2]:
                    # pprint(text)
                    styles.append('red')
                    # styles.append('red')
                # elif text[0] == text[1]:
                    # print '=='
                    # pprint(text)
                # else:
                #     print 'else'
                #     pprint(text)
                # raw_input('pause')
            text = text[-1]

        # Automatic styles
        if state and selected_state == state:
            styles.append('background')
        if state and state.optimized == 'w*':
            styles.append('background2')
        if styles:
            # print 'after:' + pformat(styles)
            for style in styles:
                # print 'style text and text type' + ":" + pformat(style) + str(text) + str(type(text))
                # raw_input('pause')
                if style == 'float':    # int styles should go before string styles
                    text = int(100 * text) / 100
                if style == 'title':
                    text = str(text).ljust(15)
                if style == 'bar':
                    text = str(text).ljust(8)
                if style == 'background':
                    # text = '\033[1;37;44m'+ text + '\033[0;37;48m'
                    text = '\033[1;47;44m'+ text + '\033[0;37;48m'
                if style == 'background2':
                    # text = '\033[1;37;45m'+ text + '\033[0;37;48m'
                    text = '\033[1;47;45m'+ text + '\033[0;37;48m'
                if style == 'color_and_background':
                    text = '\033[1;31;42m'+ text + '\033[0;37;48m'
                if style == 'color':
                    text = '\033[1;33;48m'+ text + '\033[0;37;48m'
                if style == 'green':
                    text = '\033[1;32;48m'+ text + '\033[0;37;48m'
                if style == 'red':
                    text = '\033[1;31;48m'+ text + '\033[0;37;48m'

        return text

    def print_status(self, selected_state):
        negative_to__the_right = False
        states_list = sorted(self.states, key=lambda x: x.r, reverse=negative_to__the_right)
        print '\n<CURRENT STATUS: ' + str(len(states_list[0].u)) + '>'
        print '****************'
        text = self.style('name', 'title', selected_state, None)
        for state in states_list:
            #aux prints:
            # print 'u[]:' + pformat(state.u)
            # print 'f[]:' + pformat(state.f)
            #done with aux prints
            text += self.style(state.name, 'bar', selected_state, state)
        print text
        text = self.style('u', 'title', selected_state, None)
        for state in states_list:
            text += self.style(state.u, ['float', 'bar'], selected_state, state)
        print text
        text = self.style('v', 'title', selected_state, None)
        for state in states_list:
            text += self.style(state.v, ['float', 'bar'], selected_state, state)
        print text
        text = self.style('m', 'title', selected_state, None)
        for state in states_list:
            text += self.style(state.m, ['float', 'bar'], selected_state, state)
        print text
        text = self.style('c', 'title', selected_state, None)
        for state in states_list:
            text += self.style(state.c, ['float', 'bar'], selected_state, state)
        print text
        text = self.style('r', 'title', selected_state, None)
        for state in states_list:
            text += self.style(state.r, ['float', 'bar', 'color'], selected_state, state)
        print text
        text = self.style('p', 'title', selected_state, None)
        for state in states_list:
            text += self.style(state.p, ['float', 'bar'], selected_state, state)
        text += '\n' + self.style('optimum', 'title', selected_state, None)
        for state in states_list:
            text += self.style(state.optimum, 'bar', selected_state, state)
        text += '\n' + self.style('optimized', 'title', selected_state, None)
        for state in states_list:
            text += self.style(state.optimized, 'bar', selected_state, state)
        text += '\n' + self.style('f', 'title', selected_state, None)
        for state in states_list:
            now = state.f[-1]
            if len(state.u) > 1:
                before = state.f[-2]    #start coloring when there are at least two u
                text += self.style([before, now], ['float', 'bar'], selected_state, state)
            else:
                text += self.style(now, ['float', 'bar'], selected_state, state)
        text += '\n' + self.style('%opt', 'title', selected_state, None)
        for state in states_list:
            now = 1 - state.optimum + (2 * state.optimum - 1) * state.f[-1]
            if len(state.u) > 1:
                before = 1 - state.optimum + (2 * state.optimum - 1) * state.f[-2]
                text += self.style([before, now], ['float', 'bar'], selected_state, state)
            else:
                text += self.style(now, ['float', 'bar'], selected_state, state)
        text += '\n' + self.style('r_utility', 'title', selected_state, None)
        for state in states_list:
            now = state.p * state.f[-1] * state.u[-1]
            if len(state.u) > 1:
                before = state.p * state.f[-2] * state.u[-2]
                text += self.style([before, now], ['float', 'bar'], selected_state, state)
            else:
                text += self.style(now, ['float', 'bar'], selected_state, state)
        text += '\n' + self.style('m_utility', 'title', selected_state, None)
        for state in states_list:
            now = state.p * state.f[-1] * state.m
            if len(state.u) > 1:
                before = state.p * state.f[-2] * state.m
                text += self.style([before, now], ['float', 'bar'], selected_state, state)
            else:
                text += self.style(now, ['float', 'bar'], selected_state, state)
        r_utility, s_utility, m_utility = self.update_utilities()
        text += '\n' + self.style('r_util_sum', 'title', selected_state, None)
        text += str(int(r_utility * 100) /100)
        text += '\n' + self.style('m_util_sum', 'title', selected_state, None)
        text += str(int(m_utility * 100) /100)
        text += '\n' + self.style('s_util_sum', 'title', selected_state, None)
        text += str(int(s_utility * 100) /100)
        print text

    def save_u_all_states(self):
        for state in self.states:
            state.u.append(state.trans_u)

    def save_f_all_states(self):
        for state in self.states:
            state.f.append(state.trans_f)
            # print 'f[] len'+str(len(state.f))+':'+pformat(state.f)+', trans_f:'+pformat(state.trans_f)

    def update_utilities(self):
        r_utility = 0
        s_utility = 0
        m_utility = 0
        for state in self.states:
            # multiply by probability if not uniform
            r_utility += state.p * state.trans_f * state.trans_u
            s_utility += state.p * state.trans_f * state.v
            m_utility += state.p * state.trans_f * state.m
        self.r_utility = r_utility
        self.s_utility = s_utility
        self.m_utility = m_utility
        return r_utility, s_utility, m_utility

    def calculate_ic_threshold_for_a1(self): # ic threshold for a2 is 0
        min_r_utility = 0
        for state in self.states:
            min_r_utility += state.p * state.trans_u
        return min_r_utility

    def reset_all_state_optimizations(self):
        for state in self.states:
            state.reset_optimization()

    def optimize_one_state(self):
        if show_opt_steps:
            print '\n<OPTIMIZING A STATE>'
            print '********************'
        selected = None
        for state in self.states:
            if not selected:
                if state.optimized == 'R_OPT':
                    if show_opt_steps: print 'default exist, selected', state.name
                    selected = state
            if state.optimized == 'R_OPT' and state.r > selected.r:
                if show_opt_steps: print 'changed to', state.name
                selected = state

        if selected:
            if show_opt_steps: print 'optimizing', selected.name
            selected.update_f(selected.optimum)
            return selected
        else:
            print 'nothing was selected - no R-OPT states. Sender gets maximum payoff.'
            return None

    def optimize_all_states(self, selected_state, threshold):  # all states
        self.reset_all_state_optimizations()
        self.save_u_all_states()
        delta_r_utility = None
        last_r_utility = None
        current_r_utility = self.update_utilities()[0]
        sender_maximum_payoff = False
        while current_r_utility > threshold:
            last_r_utility = self.r_utility
            last = self.optimize_one_state()
            if last is None:
                sender_maximum_payoff = True
                break
            current_r_utility = self.update_utilities()[0]
            delta_r_utility = last_r_utility - current_r_utility
            # print last_r_utility, current_r_utility, delta_r_utility
            if current_r_utility > threshold:
                if show_opt_steps:
                    print 'IC threshold not reached'
                    self.print_status(selected_state)
            else:
                print 'IC threshold reached'

        if not sender_maximum_payoff:   #if w* exists, calculate its likelihood
            if show_opt_steps: print 'calculating f(w*)'
            if last.optimum == 1:
                last.update_f((last_r_utility - threshold) / delta_r_utility)
            elif last.optimum == 0:
                last.update_f(1 - (last_r_utility - threshold) / delta_r_utility)

        # saving f,u for all states:
        self.save_f_all_states()    #f prints updated only when sender optimization is done

        self.print_status(selected_state)


class User_interface:
    def __init__(self, multiple_data):
        self.multiple_data = multiple_data
        self.data1 = self.multiple_data[0]    #duplicate data for running 2 thresholds, either can be used here
                                              #it only matters for print colors to be correct
        self.data2 = self.multiple_data[1]

    def choose_state(self):
        try:
            name = str(input('Choose state by name (0 to quit): '))
            for state1 in self.data1.states:
                if name == str(state1.name):
                    #find the same state in the other data
                    for state2 in self.data2.states:
                        if name == str(state2.name):
                            return state1, state2
        except Exception:
            print 'Bad input!'

    def choose_value(self):
        try:
            value = float(input('Choose a value (0 to quit): '))
            if value == 0:
                return None
            else:
                return value
        except Exception:
            print 'Bad input!'


class Manipulator:
    def __init__(self, ui):
        self.ui = ui
        self.multiple_data = self.ui.multiple_data

    def optimize_for_all_thresholds(self, states_1_and_2):
        thresholds = [self.multiple_data[0].calculate_ic_threshold_for_a1(), 0]
        for i in xrange(2):
            print '\n<Running Sender optimization for action a' + str(i+1) + ', IC threshold is ' +\
                str(thresholds[i]) + '>'
            if  thresholds[i] > thresholds[1-i]: #works only with 2 thresholds
                print 'This is the binding condition'
            self.multiple_data[i].optimize_all_states(states_1_and_2[i], thresholds[i])


    def run(self):
        for i in xrange(2):
            self.multiple_data[i].save_f_all_states() #adds default values to f (u is added at the begining of opimization)
        self.optimize_for_all_thresholds([None, None])
        while(True):
            state1, state2 = self.ui.choose_state()
            if state1:
                while(True):
                    self.multiple_data[0].print_status(state1)
                    self.multiple_data[1].print_status(state2)
                    print 'selected state', state1.name #it's the same name for state2 in data2
                    value = self.ui.choose_value()
                    if value:
                        print 'selected value', value
                        print 'u of state', state1.name, 'is changed to', str(value)
                        state1.update_u(value)
                        state2.update_u(value)
                        self.optimize_for_all_thresholds([state1, state2])
                    else:
                        print 'value isn\'t selected'
                        break
            else:
                print 'state isn\'t selected'
                break


if __name__ == "__main__":
    data1 = Data()
    data2 = Data()
    data = [data1, data2]
    ui = User_interface(data)
    manipulator = Manipulator(ui)
    manipulator.run()
