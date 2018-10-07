# -*- coding: utf-8 -*-
import timeit

def run_time(func):
    def wrapper(*args, **kw):
        start = timeit.default_timer()
        func(*args, **kw)
        end = timeit.default_timer() - start
        print("程序 %s 此次运行耗时: %f seconds" %(func.__name__, end))
    return wrapper