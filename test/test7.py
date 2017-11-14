from functools import wraps
from threading import Timer
import time
from datetime import datetime


def log_time_delta(func):
    @wraps(func)
    def deco():
        start = datetime.now()
        res = func()
        end = datetime.now()
        delta = end - start
        print("func runed ", delta)
        return res

    return deco


def time_limit(interval):
    def deco(func):
        def time_out():
            raise TimeoutError()

        @wraps(func)
        def deco(*args, **kwargs):
            timer = Timer(interval, time_out)
            timer.start()
            res = func(*args, **kwargs)
            return res

        return deco

    return deco


@log_time_delta
def t():
    time.sleep(2)


@log_time_delta
@time_limit(2)
def tl():
    time.sleep(100)


# t()
tl()
