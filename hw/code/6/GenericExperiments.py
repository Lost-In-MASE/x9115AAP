from __future__ import division

import sys
import random


class BaseModel:

    def __init__(self):
        self.decisions = []
        self.objectives = []
        self.constraints = []
        self.max_bound = sys.maxint
        self.min_bound = -self.lo

    def okay(self, _):
        return True

    def eval(self, model):
        if not model.scores:
            model.scores = [obj(model) for obj in model.get_objectives()]
        if model.energy is None:
            model.energy = sum(model.scores)
        return model

    def get_neighbor(self):
        return None


class Schaffer(BaseModel):

    def __init__(self):
        self.max_bound = 10**6
        self.min_bound = -self.max_bound
        self.objectives = [self.objective_one, self.objective_two]

    def eval(self, x):
        return x[0]**2 + (x - 2)**2

    def objective_one(self, model):
        return model.decs[0]**2

    def objective_two(self, model):
        return (model.decs[0] - 2)**2

    def get_objectives(self):
        return [self.objective_one, self.objective_two]

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
