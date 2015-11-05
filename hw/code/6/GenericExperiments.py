from __future__ import division

import sys
import random


class Optimizer:

    def __init__(self):
        self.something = 1


class SimulatedAnnealing(Optimizer):

    def __init__(self):
        self.something = 1


class MaxWalkSat(Optimizer):

    def __init__(self):
        self.something = 1


class BaseModel:

    def __init__(self):
        self.lo = sys.maxint
        self.hi = -self.lo

    def okay(self, _):
        return True

    def eval(self, _):
        return None

    def get_limit(self):
        return self.lo, self.hi

    def get_neighbor(self):
        return None


class Schaffer(BaseModel):

    def __init__(self):
        self.max_bound = 10**6
        self.min_bound = -self.max_bound

    def eval(self, x):
        return x[0]**2 + (x - 2)**2

    def get_neighbor(self):
        return random.randrange(self.min_bound, self.max_bound)

    def get_limit(self):
        return self.min_bound, self.max_bound

    def baselines(self):
        self.lo = eval(self.max_bound)
        self.hi = -self.lo
        for _ in range(10**6):
            cur_val = eval(self.get_neighbor())
            if cur_val < self.lo:
                self.lo = cur_val

            if cur_val > self.hi:
                self.hi = cur_val


class Osyczka(BaseModel):

    def __init__(self):
        self.something = 1