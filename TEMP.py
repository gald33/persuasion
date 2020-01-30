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
            text += str(int(100*state.f)/100).ljust(8)
        text += '\n%opt = '.ljust(15)
        for state in states_list:
            text += str(int(100*(1 - state.optimum + (2 * state.optimum - 1) * state.f)/100)).ljust(8)
	r_utility, s_utility = self.update_utilities()
        text += '\nr_utility = '.ljust(15)
        text += str(r_utility)
        text += '\ns_utility = '.ljust(15)
        text += str(s_utility)
        print text