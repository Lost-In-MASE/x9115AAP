from __future__ import division

import sys
import random
import math
import datetime


class BaseModel:

    def __init__(self):
        self.min_bound = sys.maxint
        self.max_bound = -self.min_bound
        self.lo = sys.maxint
        self.hi = -self.lo
        self.obj_fns = []
        self.constraints = None
        self.number_vars = 0
        self.var_bounds = []

    def okay(self, _):
        return True
        
    def get_neighbor(self):
        return None
        
    def normalize_val(self, value):
        return (value - self.lo)/(self.hi - self.lo)
        


class Schaffer(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self.max_bound = 10**6
        self.min_bound = -self.max_bound
        self.var_bounds = [(self.min_bound, self.max_bound)]
        self.baselines()
        self.number_vars = 1
        self.obj_fns = [self.f1, self.f2]
        
    def eval(self, x):
        return self.f1(x) + self.f2(x)
        
    def f1(self, x):
        return x**2
        
    def f2(self, x):
        return (x - 2)**2
        
    def get_baselines(self):
        return self.lo, self.hi

    def baselines(self):
        self.lo = self.eval(self.max_bound)
        self.hi = -self.lo
        for _ in range(10**6):
            cur_val = self.eval(self.get_neighbor())
            if cur_val < self.lo:
                self.lo = cur_val

            if cur_val > self.hi:
                self.hi = cur_val
                
    def get_neighbor(self):
        return random.randrange(self.min_bound, self.max_bound)


class Osyczka(BaseModel):
    
    def __init__(self):
        BaseModel.__init__(self)
        self.number_vars = 6
        self.obj_fns = [self.f1, self.f2]
        self.constraints = list()
        self.constraints.append(lambda x : x[0] + x[1] - 2)
        self.constraints.append(lambda x : 6 - x[0] - x[1])
        self.constraints.append(lambda x : 2 - x[1] + x[0])
        self.constraints.append(lambda x : 2 - x[0] + 3*x[1])
        self.constraints.append(lambda x : 4 - x[3] - (x[2] - 3)**2)
        self.constraints.append(lambda x : (x[4] - 3)**3 + x[5] - 4)
        self.var_bounds = [(0, 10), (0, 10), (1, 5), (0, 6), (1, 5), (0, 10)]
        self.baselines()
        
    def eval(self, x):
        return self.f1(x) + self.f2(x)
        
    def get_neighbor(self):
        x = list()
        for i, j in self.var_bounds:
            x.append(random.randrange(i, j))
            
        return x
    
    def okay(self, x):
        for constraint in self.constraints:
            if constraint(x) < 0:
                return False
            
        return True
        
    def f1(self, x):
        return -(25 * (x[0] - 2)**2 + (x[1] - 2)**2 + (x[2] - 1)**2 * (x[3] - 4)**2 + (x[4] - 1)**2)
        
    def f2(self, x):
        return sum([i**2 for i in x])
        
    def baselines(self):
        self.lo = sys.maxint
        self.hi = -self.lo
        
        for _ in xrange(0, 10000):
            
            while True:
                soln = self.get_neighbor()
                if (self.okay(soln)):
                    break

            energy = self.eval(soln)

            if soln > self.hi:
                self.hi = energy

            if soln < self.lo:
                self.lo = energy
                
    def get_baselines(self):
        return self.lo, self.hi
        
        
def SimulatedAnnealing(model):
    
    def get_probability(curEnergy, neighborEnergy, count):
        return math.exp((curEnergy - neighborEnergy)/count)
    
    max_bound = 10**6
    min_bound = -max_bound
    base_min, base_max = model.get_baselines()

    # Base variables
    kMax = 1000
    eMax = -.1
    output = ""

    # Start with a random value
    startVal = model.get_neighbor()
    curEnergy = model.normalize_val(model.eval(startVal))

    bestEnergy = curEnergy
    bestVal = startVal
    curVal = startVal
    i = 1
    while i < kMax - 1 and curEnergy > eMax:
        mutatedNeighbor = model.get_neighbor()
        while model.okay(mutatedNeighbor) is False:
            mutatedNeighbor = model.get_neighbor()
        
        neighborEnergy = model.normalize_val(model.eval(mutatedNeighbor))

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

def MaxWalkSat(model):
    
    def change_to_maximize(soln, index):
        evals = 0
        best = soln
        solution = soln
        low, high = model.var_bounds[index]
        delta = (high - low)/steps
        for i in xrange(0, steps):
            evals += 1
            solution[index] = low + delta*i
            if model.okay(solution) and model.eval(solution) > model.eval(best):
                best = list(solution)
        return best, evals
    
    max_tries = 100
    max_changes = 50
    p = 0.5
    threshold = 200
    steps = 10

    evals = 0
    init_soln = model.get_neighbor()

    for i in range(0, max_tries):
        output = str()
        new_soln = model.get_neighbor()
        while model.okay(new_soln) is False:
            new_soln = model.get_neighbor()

        for j in range(0, max_changes):
            result = str()
            if model.eval(new_soln) > threshold:
                return new_soln

            c = random.randint(1, model.number_vars) - 1
            if p < random.random():
                copy_list = list(new_soln)
                i, j = model.var_bounds[c]
                copy_list[c] = random.randrange(i, j)

                if model.okay(copy_list):
                    new_soln = copy_list
                    result = "?"
                else:
                    result = "."
            else:
                copy_list, t_evals = change_to_maximize(new_soln, c)
                evals += t_evals
                if copy_list == new_soln:
                    result = "+"
                    new_soln = copy_list
                else:
                    result = "."
            output += result
            if model.eval(new_soln) > model.eval(init_soln):
                init_soln = list(new_soln)

        print "Evals : " + str(evals) + " Current Best Energy : " + \
              str(model.normalize_val(model.eval(init_soln))) + " " + output

if __name__ == '__main__':
    # a = datetime.datetime.now()
    # SimulatedAnnealing(Schaffer())
    # b = datetime.datetime.now()
    # print("# Runtime: %f"  %((b - a).microseconds/1000000))
    
    a = datetime.datetime.now()
    MaxWalkSat(Osyczka())
    b = datetime.datetime.now()
    print("# Runtime: %f"  %((b - a).microseconds/1000000))