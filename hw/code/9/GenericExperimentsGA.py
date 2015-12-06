from __future__ import division

import random
import math
import sys

from sk import a12
from sk import rdivDemo

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
        self.baseline_count = 10**6

    def okay(self, _):
        return True

    def type1(self, solution, sb):
        for objective in self.get_objectives():
            if objective(solution) > objective(sb):
                return False

        return True

    def get_neighbor(self):
        x = list()
        for i, j in self.var_bounds:
            if isinstance(i, int) and isinstance(j, int):
                x.append(random.randrange(i, j))
            else:
                x.append(random.uniform(i, j))

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

        # self.hi = 100
        # self.lo = 0

    def normalize_val(self, value):
        return (value - self.lo)/(self.hi - self.lo)

    def eval(self, x):
        energy = 0
        for obj in self.get_objectives():
            energy += obj(x)

        return energy

    def get_objectives(self):
        return None

    def get_baselines(self):
        return self.lo, self.hi


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

class Golinski(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self.model_name = "Golinski"
        self.number_vars = 7
        self.constraints = list()
        self.constraints.append(lambda x: ((x[0] * (x[1] ** 2) * x[2]) ** -1 - 27 ** -1) <= 0)
        self.constraints.append(lambda x: ((x[0] * (x[1] ** 2) * (x[2] ** 2)) ** -1 - 397.5 ** -1) <= 0)
        self.constraints.append(lambda x: ((x[3] ** 3/(x[1] * x[2] ** 2 * x[5] ** 4)) - 1.93 ** -1) <= 0)
        self.constraints.append(lambda x: x[4] ** 3/(x[1] * x[2] * x[6] ** 4) - 1/1.93 <= 0)
        self.constraints.append(lambda x: x[1] * x[2] <= 0)
        self.constraints.append(lambda x: (x[0] / x[1]) - 12 <= 0)
        self.constraints.append(lambda x: 5 - (x[0] / x[1]) <= 0)
        self.constraints.append(lambda x: 1.9 - x[3] + 1.5 * x[5] <= 0)
        self.constraints.append(lambda x: 1.9 - x[4] + 1.1 * x[6] <= 0)
        self.constraints.append(lambda x: self.f2(x) <= 1300)
        self.constraints.append(lambda x: (((745 * x[4]/(x[1] * x[2])) ** 2 + 1.575 * 10**8) ** 0.5) /
                                          (0.1 * x[6] ** 3) <= 1100)
        self.var_bounds = [(2.6, 3.6), (0.7, 0.8), (17, 28), (7.3, 8.3), (7.3, 8.3), (2.9, 3.9), (5, 5.5)]
        self.baselines()

    def f2(self, x):
        return ((745 * x[3] / (x[1] * x[2])) ** 2 + 1.69 * 10 ** 7) ** 0.5 / (0.1 * x[5] ** 3)

    def get_objectives(self):
        return [
            lambda x: 0.7854 * x[0] * (x[1]**2) * (10*(x[2]**2)/3 + 14.933*x[2] - 43.0934) - 1.508 * x[0] * (x[5]**2 + x[6]**2) + 7.477 * (x[5]**3 + x[6]**3) + 0.7854 * (x[3] * (x[5] ** 2) + x[4] * (x[6] ** 2)),
            self.f2
        ]

    def okay(self, x):
        for constraint in self.constraints:
            if constraint(x) < 0:
                return False

        return True


class DTLZ1(BaseModel):
    def __init__(self, num_dec, num_obj):
        BaseModel.__init__(self)
        self.model_name = "DTLZ1"
        self.number_vars = num_dec
        self.number_obj = num_obj
        self.var_bounds = []
        for _ in xrange(self.number_vars):
            self.var_bounds.append((0.0, 1.0))
        self.baselines()

    def gx(self, x):
        g = 0.0
        for i in xrange(0, self.number_vars):
            g += math.pow(x[i] - 0.5, 2) - math.cos(20 * math.pi * (x[i] - 0.5))
        g = 100 * (g + self.number_vars)
        return g

    def obj(self, x, i):
        result = 0.5 * (1 + self.gx(x))
        for j in xrange(0, self.number_obj - (i + 1)):
            result *= x[j]
        if (i != 0):
            result *= 1 - x[self.number_obj - (i + 1)]
        return result

    def get_objectives(self):
        f = [None] * self.number_obj
        for i in xrange(0, self.number_obj - 1):
            f[i] = lambda x: self.obj(x, i)
        return f


class DTLZ3(BaseModel):
    def __init__(self, num_dec, num_obj):
        BaseModel.__init__(self)
        self.model_name = "DTLZ3"
        self.number_vars = num_dec
        self.number_obj = num_obj
        self.var_bounds = []
        for _ in xrange(self.number_vars):
            self.var_bounds.append((0.0, 1.0))
        self.baselines()

    def gx(self, x):
        g = 0.0
        for i in xrange(0, self.number_vars):
            g += math.pow(x[i] - 0.5, 2) - math.cos(20 * math.pi * (x[i] - 0.5))
        g = 100 * (g + self.number_vars)
        return g

    def obj(self, x, i):
        result = 1 + self.gx(x)
        for j in xrange(0, self.number_obj - (i + 1)):
            result *= math.cos(x[j] * math.pi * 0.5)
        if (i != 0):
            result *= math.sin(x[self.number_obj - (i + 1)] * math.pi * 0.5)
        return result

    def get_objectives(self):
        f = [None] * self.number_obj
        for i in xrange(0, self.number_obj):
            f[i] = lambda x: self.obj(x, i)
        return f


class DTLZ5(BaseModel):
    def __init__(self, num_dec, num_obj):
        BaseModel.__init__(self)
        self.model_name = "DTLZ5"
        self.number_vars = num_dec
        self.number_obj = num_obj
        self.var_bounds = []
        for _ in xrange(self.number_vars):
            self.var_bounds.append((0.0, 1.0))
        self.baselines()

    def gx(self, x):
        g = 0.0;
        for i in xrange(0, self.number_vars):
            g += math.pow(x[i] - 0.5, 2)
        return g

    '''Verify the theta function g(r) is not defined'''
    def theta(self, x, i):
        if (i == 0):
            return x[0]
        else:
            g = self.gx(x)
            t = 1 / (2 * (1 + g))
            return t + ((g * x[i]) / (1 + g))

    def obj(self, x, i):
        result = 1 + self.gx(x)
        for j in xrange(0, self.number_obj - (i + 1)):
            result *= math.cos(self.theta(x, j) * math.pi * 0.5)
        if (i != 0):
            result *= math.sin(self.theta(x, self.number_obj - (i + 1)) * math.pi * 0.5)
        return result

    def get_objectives(self):
        f = [None] * self.number_obj
        for i in xrange(0, self.number_obj):
            f[i] = lambda x: self.obj(x, i)
        return f

class DTLZ7(BaseModel):


    def __init__(self, num_dec, num_obj):
        BaseModel.__init__(self)
        self.model_name = "DTLZ7"
        self.number_vars = num_dec
        self.number_obj = num_obj
        self.var_bounds = []
        for _ in xrange(self.number_vars):
            self.var_bounds.append((0.0, 1.0))
        self.baselines()

    def gx(self, x):
        y = 0.0
        for i in xrange(0, self.number_vars):
            y += x[i]
        return(9*y/self.number_vars)

    def hx(self, f, g, x):
        y = 0.0
        for i in xrange(0, self.number_obj - 1):
            y += (f[i](x) / (1 + g)) * (1 + math.sin(3 * math.pi * f[i](x)))
        return self.number_obj - y

    def last_obj(self, x, f):
        g = 1 + self.gx(x)
        res = (1 + g) * self.hx(f, g, x)
        return res

    def obj(self, x, i):
        return x[i]

    def get_objectives(self):
        f = [None] * self.number_obj
        for i in xrange(0, self.number_obj - 1):
            f[i] = lambda x : self.obj(x, i)
        f[self.number_obj - 1] = lambda x : self.last_obj(x, f)

        return f

def genetic_algorithm(model):
    population_size = model.number_vars * 10
    mutate_prob = 0.05
    cross_prob = 0.90
    k_max = 1000

    def build_population():
        new_population = []
        for _ in xrange(population_size):
            neighbor = model.get_neighbor()
            while model.okay(neighbor) is False:
                neighbor = model.get_neighbor()
            new_population.append(neighbor)

        return new_population

    def type2(era_one, era_two, model):
        for objective in model.get_objectives():
            era_one_objective = []
            era_two_objective = []
            for i in xrange(0, len(era_one)):
                era_one_objective.append(objective(era_one[i]))
                era_two_objective.append(objective(era_two[i]))
            if (a12(era_one_objective, era_two_objective) > 0.5):
                return 10

        return -1

    def mutate(candidate):
        for i in xrange(model.number_vars):
            if random.random() < mutate_prob:
                l, h = model.var_bounds[i]
                candidate[i] = random.uniform(l, h)

    def cross_over(parent1, parent2):
        cross_point = random.randint(0, model.number_vars - 1)
        child1 = []
        child2 = []
        for i in xrange(0, cross_point):
            child1.append(parent1[i])
            child2.append(parent2[i])

        for i in xrange(cross_point, model.number_vars):
            child1.append(parent2[i])
            child2.append(parent1[i])

        return (child1, child2)

    def select(population):
        pool = []
        dominated = []
        for c1 in xrange(population_size):
            if c1 in dominated:
                continue
            for c2 in xrange(population_size):
                if c1 == c2:
                    continue
                if(model.type1(population[c1], population[c2])):
                    # print "Binary Dominated:", c1
                    if c1 not in pool:
                        pool.append(c1)
                    if c2 not in dominated:
                        dominated.append(c2)
                    if c2 in pool:
                        pool.remove(c2)
        # print len(pool)
        if(len(pool) == 0):
            # print "Length of pool is 0"
            return range(0, population_size)
        return pool

    def bdom_better(c1, c2):
        cobj1 = []
        cobj2 = []
        for objective in model.get_objectives():
            cobj1.append(objective(c1))
            cobj2.append(objective(c2))
        better = any([x < y for x,y in zip(cobj1, cobj2)])
        worse = any([x > y for x,y in zip(cobj1, cobj2)])
        return better and not worse

    print "Model Name : " + model.model_name + ", Optimizer : Genetic Algorithm"
    population = build_population()
    best_sol = model.normalize_val(model.eval(population[0]))
    sumofpop = 0
    for i in population:
        sumofpop += model.eval(i)
    best_avg_sol = sumofpop / population_size
    avg_energy = []
    avg_energy.append(best_avg_sol)

    era = 100
    min_sol = best_sol
    for gen_count in xrange(k_max):
        k = 0
        next_gen = []
        best_pool = select(population)
        # print ""
        # print ""
        # for i in best_pool:
        #     print model.normalize_val(model.eval(population[i]))
        # print best_pool
        for _ in xrange(0,population_size,2):

            parent1 = population[best_pool[random.randint(0, len(best_pool) - 1)]]
            parent2 = population[best_pool[random.randint(0, len(best_pool) - 1)]]
            if random.random() < cross_prob:
                child1, child2 = cross_over(parent1, parent2)
                mutate(child1)
                mutate(child2)
            else:
                child1, child2 = parent1, parent2

            next_gen.append(child1)
            next_gen.append(child2)
            energy1 = model.eval(child1)
            energy2 = model.eval(child2)

            '''Update best solution'''
            if energy1 < min_sol:
                min_sol = energy1

            if energy2 < min_sol:
                min_sol = energy2
            k += energy1
            k += energy2

        # if(min_sol <= threshold):
        #     break
        # elif(min_sol < best_sol):
            best_sol = min_sol
        if gen_count > 100:
            era += type2(population, next_gen, model)

        if era == 0:
            print "Early Termination -", gen_count + 1, " number of generations"
            print "Best Energy: ", best_sol, " | Average Energy: ", best_avg_sol
            break

        population = next_gen
        avg_energy.append(k/population_size)

        if(k/population_size < best_avg_sol):
            best_avg_sol = k/population_size

        energies = []
        for i in xrange(population_size):
            #print ("%.5f \n" % (model.normalize_val(model.eval(population[i]))))
            energies.append(model.eval(population[i]))
        energies.sort()
        # print energies

        sum = 0
        #Calculate the percentage of population that are similar
        for i in xrange(1, len(energies)):
            if energies[i] == energies[i-1]:
                sum += 1
        # print sum/population_size

    # print "Best Energy: ", best_sol, " | Average Energy: ", best_avg_sol, "Length of Population: "
    return population
    # print avg_energy

if __name__ == '__main__':

    era_collection = []
    decisions = [10, 20, 40]
    objectives = [2, 4, 6, 8]
    # decisions = [10, 20]
    # objectives = [2]
    models = [DTLZ7]
    model_text = ["DTLZ7"]

    for model_type, text in zip(models, model_text):
        for decs in decisions:
            for objs in objectives:
                model = model_type(decs, objs)
                era_val = [model.eval(val) for val in genetic_algorithm(model)]
                era_val.insert(0, text + "_" + str(decs) + "_" + str(objs))
                era_collection.append(era_val)
    models = [Osyczka, Kursawe, Golinski]
    model_text = ["OSYCZ", "KURSA", "GOLIN"]
    for model_type, text in zip(models, model_text):
        model = model_type()
        era_val = [model.eval(val) for val in genetic_algorithm(model)]
        era_val.insert(0, text)
        era_collection.append(era_val)
    # print era_collection
    print rdivDemo(era_collection)