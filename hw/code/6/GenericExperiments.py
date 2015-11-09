from __future__ import division

import random
import math
import datetime
import sys


class BaseModel:

    def __init__(self):
        self.model_name = None
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
        self.model_name = "Schaffer"
        self.baseline_count = 10**6
        self.number_vars = 1
        self.max_bound = 10**4
        self.min_bound = -self.max_bound
        self.var_bounds = [(self.min_bound, self.max_bound)]
        self.baselines()

    def get_objectives(self):
        return [lambda x: x[0]**2, lambda x: (x[0] - 2)**2]


class Osyczka(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self.model_name = "Osyczka"
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
        self.model_name = "Kursawe"
        self.number_vars = 3
        self.max_bound = 5
        self.min_bound = -self.max_bound
        self.var_bounds = [(self.min_bound, self.max_bound) for _ in xrange(self.number_vars)]
        self.baselines()

    def get_objectives(self):
        return [
            lambda x: (-10 * math.exp(-0.2 * math.sqrt(x[0] ** 2 + x[1] ** 2)) +
                       (-10 * math.exp(-0.2 * math.sqrt(x[1] ** 2 + x[2] ** 2)))),
            lambda x: sum([(abs(i) ** 0.8 + 5 * math.sin(i)) for i in x])]


def simulated_annealing(model):
    
    def get_probability(cur_energy, neighbor_energy, count):
        return math.exp((cur_energy - neighbor_energy)/count)

    print "Model Name : " + model.model_name + ", Optimizer : simulated annealing"
    
    # Base variables
    kMax = 1000
    eMax = -.1
    output = ""

    # Start with a random value
    start_val = model.get_neighbor()
    cur_energy = model.normalize_val(model.eval(start_val))

    best_energy = cur_energy
    best_val = start_val
    cur_val = start_val
    i = 1
    while i < kMax - 1 and cur_energy > eMax:
        mutated_neighbor = model.get_neighbor()
        while model.okay(mutated_neighbor) is False:
            mutated_neighbor = model.get_neighbor()
        
        neighbor_energy = model.normalize_val(model.eval(mutated_neighbor))

        if neighbor_energy < best_energy:
            best_energy = neighbor_energy
            best_val = mutated_neighbor
            output += "!"

        if neighbor_energy < cur_energy:
            cur_energy = neighbor_energy
            cur_val = mutated_neighbor
            output += "+"

        elif get_probability(cur_energy, neighbor_energy,  (1 - i/kMax)**10) > random.random():
            cur_val = mutated_neighbor
            cur_energy = neighbor_energy
            output += "?"
        else:
            output += "."

        if i % 25 == 0:
            print ("%6d : %.5f,  %25s" % (i, best_energy, output))
            output = ""
            cur_energy = 1

        i += 1

    print(": e %f" % best_energy)


def max_walk_sat(model):

    def change_to_maximize(soln, index):
        evaluations = 0
        best = soln
        solution = soln
        low, high = model.var_bounds[index]
        delta = (high - low)/steps
        for k in xrange(0, steps):
            evaluations += 1
            solution[index] = low + delta*k
            if model.okay(solution) and model.eval(solution) > model.eval(best):
                best = list(solution)
        return best, evaluations

    print "Model Name : " + model.model_name + ", Optimizer : max walk sat"
    
    max_tries = 100
    max_changes = 50
    p = 0.5
    threshold = 1
    steps = 10

    evals = 0
    init_soln = model.get_neighbor()
    while model.okay(init_soln) is False:
        init_soln = model.get_neighbor()

    for i in xrange(0, max_tries):
        output = str()
        new_soln = model.get_neighbor()
        while model.okay(new_soln) is False:
            new_soln = model.get_neighbor()

        for j in xrange(0, max_changes):
            result = str()
            if model.normalize_val(model.eval(new_soln)) > threshold:
                print("\nBest Solution : " + str(init_soln))
                print("Best Energy : " + str(model.normalize_val(model.eval(init_soln))))
                return

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
                copy_list, t_evals = change_to_maximize(list(new_soln), c)
                evals += t_evals
                if copy_list == new_soln:
                    result = "."
                else:
                    new_soln = copy_list
                    result = "+"
            output += result
            if model.eval(new_soln) > model.eval(init_soln):
                init_soln = list(new_soln)

        print "Evals : " + str(evals) + " Current Best Energy : " + \
              str(model.normalize_val(model.eval(init_soln))) + " " + output

    print("\nBest Solution : " + str(init_soln))
    print("Best Energy : " + str(model.normalize_val(model.eval(init_soln))))

if __name__ == '__main__':
    # a = datetime.datetime.now()
    # simulated_annealing(Kursawe())
    # b = datetime.datetime.now()
    # print("# Runtime: %f" % ((b - a).microseconds/1000000))

    # a = datetime.datetime.now()
    # max_walk_sat(Kursawe())
    # b = datetime.datetime.now()
    # print("# Runtime: %f" % ((b - a).microseconds/1000000))

    for software_model in [Schaffer, Osyczka, Kursawe]:
        for optimizer in [simulated_annealing, max_walk_sat]:
            print "\n\n------------------------------------------------------------\n\n"
            optimizer(software_model())
