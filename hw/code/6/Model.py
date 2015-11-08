from math import sin
from math import exp
from math import sqrt
import sys
import random


class BaseModel:

    def __init__(self):
        self.min_bound = sys.maxint
        self.max_bound = -self.min_bound
        self.lo = sys.maxint
        self.hi = -self.lo
        self.constraints = None
        self.number_vars = 0
        self.var_bounds = []
        self.baseline_count = 10**4

    def okay(self, _):
        return True

    def get_neighbor(self):
        x = list()
        for i, j in self.var_bounds:
            x.append(random.randrange(i, j))

        return x

    def baselines(self):
        self.lo = sys.maxint
        self.hi = -self.lo

        for _ in xrange(0, 10000):

            while True:
                soln = self.get_neighbor()
                if self.okay(soln):
                    break

            energy = self.eval(soln)

            if energy > self.hi:
                self.hi = energy

            if energy < self.lo:
                self.lo = energy

    def normalize_val(self, value):
        return (value - self.lo)/(self.hi - self.lo)

    def eval(self, x):
        energy = 0
        for obj in self.get_objectives():
            energy += obj(x)

        return energy

    def get_objectives(self):
        return self.obj_fns

    def baselines(self):
        self.lo = sys.maxint
        self.hi = -self.lo

        for _ in xrange(0, 10000):

            while True:
                soln = self.get_neighbor()
                if self.okay(soln):
                    break

            energy = self.eval(soln)

            if energy > self.hi:
                self.hi = energy

            if energy < self.lo:
                self.lo = energy

    def get_baselines(self):
        return self.lo, self.hi


class Schaffer(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self.baseline_count = 10**6
        self.number_vars = 1
        self.max_bound = 10**6
        self.min_bound = -self.max_bound
        self.var_bounds = [(self.min_bound, self.max_bound)]
        self.baselines()

    def get_objectives(self):
        return [lambda x: x[0]**2, lambda x: (x[0] - 2)**2]


class Osyczka(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self.number_vars = 6
        self.constraints = list()
        self.constraints.append(lambda x: x[0] + x[1] - 2)
        self.constraints.append(lambda x: 6 - x[0] - x[1])
        self.constraints.append(lambda x: 2 - x[1] + x[0])
        self.constraints.append(lambda x: 2 - x[0] + 3*x[1])
        self.constraints.append(lambda x: 4 - x[3] - (x[2] - 3)**2)
        self.constraints.append(lambda x: (x[4] - 3)**3 + x[5] - 4)
        self.var_bounds = [(0, 10), (0, 10), (1, 5), (0, 6), (1, 5), (0, 10)]
        self.baselines()

    def get_objectives(self):
        return [
            lambda x: -(25 * (x[0] - 2)**2 + (x[1] - 2)**2 + (x[2] - 1)**2 * (x[3] - 4)**2 + (x[4] - 1)**2),
            lambda x: sum([i**2 for i in x])]

    def okay(self, x):
        for constraint in self.constraints:
            if constraint(x) < 0:
                return False

        return True


class Kursawe(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self.number_vars = 3
        self.max_bound = 5
        self.min_bound = -self.max_bound
        self.var_bounds = [(self.min_bound, self.max_bound) for _ in xrange(0, 3)]
        self.baselines()

    def get_objectives(self):
        return [
            lambda x: (-10 * exp(-0.2 * sqrt(x[0] ** 2 + x[1] ** 2)) + -10 * exp(-0.2 * sqrt(x[1] ** 2 + x[2] ** 2))),
            lambda x: sum([(abs(i) ** 0.8 + 5 * sin(i ** 3)) for i in x])]
