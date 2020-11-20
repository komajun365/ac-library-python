import random


# from ../utils/random.hpp
def randpair(lower, upper):
    assert upper - lower >= 1
    a, b = 0, 0
    while a==b:
        a = random.randint(lower, upper)
        b = random.randint(lower, upper)
    if a > b:
        a, b = b, a
    return a, b