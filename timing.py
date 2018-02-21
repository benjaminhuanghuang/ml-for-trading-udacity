import numpy as np
from time import time


def how_long( func, *args):
    t0 = time()
    result = func(args)
    t1 = time()
    retrun result, t1 - t0


    