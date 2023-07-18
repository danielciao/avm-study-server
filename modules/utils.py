import time

import numpy as np


def safe_div(x, y):
    return x / y if y != 0 else np.nan


def format_ratio(dividend, divisor):
    return '%.4f' % (dividend * 100 / divisor) + '%'


class Timer:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def log(self, message):
        elapsed_time = time.perf_counter() - (self.start_time or 0)
        print(f'=== {message} ({elapsed_time:0.4f}s) ===')

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        pass
