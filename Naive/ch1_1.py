from __future__ import annotations

import datetime
import time
from typing import Generator

import functools
from functools import lru_cache, wraps
from random import randint
import timeit


def fib_naive(n: int) -> int:
    if n < 2:
        return n
    else:
        return fib_naive(n - 1) + fib_naive(n - 2)


def fib_statefull(n: int, state=None) -> int:
    """Statefull doesn't need to recalculate encountered values"""
    if not state:
        state = {0: 0, 1: 1, 2: 1}
    if n in state.keys():
        return state[n]
    else:
        return fib_statefull(n - 1, state) + fib_statefull(n - 2, state)


@functools.lru_cache(maxsize=None)
def fib_auto_cache(n: int) -> int:
    """lru cache - LastRecentlyUsed basically state created and managed by interpreter"""
    return 2 if n < 2 else (fib_auto_cache(n - 1) + fib_auto_cache(n - 2))


def fib_iterative(n: int) -> int:
    """Iterable solution is even better course it O(n)"""
    if n == 0: return n
    last = 0
    next = 1
    for _ in range(1, n):
        last, next = next, last + next
    return next


def fib_gen(n: int) -> Generator[int, None, None]:
    """As soon as we know iterative step, we can construct generator"""
    yield 0  # 0
    if n > 0: yield 1  # 1
    last = 0
    next = 1
    for _ in range(1, n):
        last, next = next, last + next
    yield next


def timing(f):
    """Generator can't be passed to timeit by partial wrapper,
    so we create decorator wrapper"""

    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % \
              (f.__name__, args, kw, te - ts))
        return result

    return wrap


def run_tests(amount=5, limit=32) -> None:
    fib_vars = {'naive': fib_naive,
                'statefull': fib_statefull,
                'lru_cache': lru_cache,
                'iterative': fib_iterative}

    n = randint(0, limit)
    for k, v in fib_vars.items():
        print(f"Timing {k} for {n} with timeit {amount} times")
        if n > 25 and k == 'naive':
            print(f"Ignoring naive course {n} to big")
            continue
        t = timeit.Timer(functools.partial(v, n))
        print(t.timeit(amount))

def manual_timing_of_gen(limit=32):
    n = randint(0, limit)
    print("To lazy to write generator wrapper, so")
    st = datetime.datetime.now()
    for i in fib_gen(n):
        print(i)
    end = datetime.datetime.now()
    td = end - st
    print(f"With printing took {td} for {n}")


if __name__ == "__main__":
    run_tests(5)
    #print(fib_statefull(15))
    ...
