import matplotlib.pyplot as plt
import math
from pprint import pprint
import numpy as np


def find_root(v):
    a = 2 * (v - 1)
    return (math.sqrt(math.pow(a, 2) - 4*v -3) - 1)/a


def n_h(v, p, action):
    if action == 'hide':
        return (v-1)*p + 1
    elif action == 'share':
        return (v-1)*p


def utility_for_hide(v, p):
    return 2*float(v - n_h(v, p, 'hide'))/(v * (v + n_h(v, p, 'hide')))


def utility_for_share(v, p):
    return 1*float(v - n_h(v, p, 'share'))/(v * (v + n_h(v, p, 'share')))


def compare_utilities(v):
    p = find_root(v)
    # print(utility_for_hide(v, p))
    # print(utility_for_share(v, p))
    print 'v =', v, ', p =', p, ', u(hide) =', utility_for_hide(v, p), ', delta utility =',\
          utility_for_hide(v, p) - utility_for_share(v, p)


def compare_many_utilities(v__low, v_high):
    for v in range(v__low, v_high + 1):
        compare_utilities(v)


compare_many_utilities(4, 1000)

def plot():
    x = range(4, 1001)
    y = []
    for num in x:
        y.append(find_root(num))

    pprint(x)
    pprint(y)

    plt.plot(x, y, 'ro')
    plt.axis([0, max(x), 0, 1])
    plt.savefig('output.png')
    plt.show()
