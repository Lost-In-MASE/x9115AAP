from __future__ import division
import random
import math
import datetime


def normalize_val(value, low_val, high_val):
    return (get_shaffer_objective_value(value) - low_val) / (high_val - low_val)


def get_shaffer_objective_value(value):
    return value**2 + (value - 2)**2


def get_base_schaffer_values(min_bound, max_bound):
    low_val = get_shaffer_objective_value(max_bound)
    high_val = -low_val
    for _ in range(10000):
        cur_val = get_shaffer_objective_value(random.randrange(min_bound, max_bound))
        if cur_val < low_val:
            low_val = cur_val

        if cur_val > high_val:
            high_val = cur_val

    return low_val, high_val


def get_probability(curEnergy, neighborEnergy, count):
    return math.exp((curEnergy - neighborEnergy)/count)


def start_shaffer():
    max_bound = 10**2
    min_bound = -max_bound
    base_min, base_max = get_base_schaffer_values(min_bound, max_bound)

    # Base variables
    kMax = 1000
    eMax = -.1
    output = ""

    # Start with a random value
    startVal = random.randrange(min_bound, max_bound)
    curEnergy = normalize_val(startVal, base_min, base_max)

    bestEnergy = curEnergy
    bestVal = startVal
    curVal = startVal
    i = 1
    while i < kMax - 1 and curEnergy > eMax:
        mutatedNeighbor = random.randrange(min_bound, max_bound)
        neighborEnergy = normalize_val(mutatedNeighbor, base_min, base_max)

        if neighborEnergy < bestEnergy:
            bestEnergy = neighborEnergy
            bestVal = mutatedNeighbor
            output += "!"

        if neighborEnergy < curEnergy:
            curEnergy = neighborEnergy
            curVal = mutatedNeighbor
            output += "+"

        elif get_probability(curEnergy, neighborEnergy,  (1 - i/kMax)**10) > random.random():
            curVal = mutatedNeighbor
            curEnergy = neighborEnergy
            output += "?"
        else:
            output += "."

        if i % 25 == 0:
            print ("%6d : %.5f,  %25s" % (i, bestEnergy, output))
            output = ""
            curEnergy = 1

        i += 1

    print(": e %f" %curEnergy)


if __name__ == '__main__':
    a = datetime.datetime.now()
    start_shaffer()
    b = datetime.datetime.now()
    print("# Runtime: %f"  %((b - a).microseconds/1000000))
