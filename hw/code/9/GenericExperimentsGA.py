from __future__ import division

import random
import math
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


def genetic_algorithm(model):
    population_size = 100
    mutate_prob = 0.05
    k_max = 1000

    def build_population():
        new_population = []
        for _ in xrange(population_size):
            neighbor = model.get_neighbor()
            while model.okay(neighbor) is False:
                neighbor = model.get_neighbor()
            new_population.append(neighbor)

        return new_population

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
            child1[i] = parent1[i]
            child2[i] = parent2[i]

        for i in xrange(cross_point, model.number_vars):
            child1[i] = parent2[i]
            child2[i] = parent1[i]

        return (child1, child2)

    def select(population):
        pool = []
        used = []

        for _ in xrange(population_size/2):
            c1 = random.randint(0, population_size)
            while(c1 in used):
                c1 = random.randint(0, population_size)

            c2 = random.randint(0, population_size)
            while(c1 in used):
                c2 = random.randint(0, population_size)

            used.append(c1)
            used.append(c2)

            if model.eval(population[c1]) > model.eval(population[c2]):
                pool.append(c1)
            else:
                pool.append(c2)

        return pool

    print "Model Name : " + model.model_name + ", Optimizer : Genetic Algorithm"
    population = build_population()
    best_sol = model.eval(population[0])

    for _ in xrange(k_max):
        next_gen = []
        best_pool = select(population)

        for _ in xrange(population_size/2):
            parent1 = population[best_pool[random.randint(0, population_size/2)]]
            parent2 = population[best_pool[random.randint(0, population_size/2)]]
            child1, child2 = cross_over(parent1, parent2)
            mutate(child1)
            mutate(child2)
            next_gen.append(child1)
            next_gen.append(child2)

            '''Update best solution'''
            if model.eval(child1) > best_sol:
                best_sol = model.eval(child1)
            if model.eval(child2) > best_sol:
                best_sol = model.eval(child2)


        population = next_gen



def differential_evolution(model):

    def build_frontier():
        new_frontier = []
        for _ in xrange(100):
            neighbor = model.get_neighbor()
            while model.okay(neighbor) is False:
                neighbor = model.get_neighbor()
            new_frontier.append(neighbor)

        return new_frontier
        
    def get_frontier_neighbors(cur):
        seen = []
        while len(seen) < 3:
            rand_index = random.randint(0, 99)
            if rand_index == cur:
                continue
            if rand_index not in seen:
                seen.append(rand_index)
                
        return seen

    def get_mutation(seen):
        soln = []
        for j in xrange(model.number_vars):
            l , m = model.var_bounds[j]
            inter = (frontier[seen[0]][j] + 0.75 * (frontier[seen[1]][j] - frontier[seen[2]][j]))
            if inter >= l and inter <= m:
                soln.append(inter)
            else:
                soln.append(frontier[seen[random.randint(0, 2)]][j])
        return soln


    print "Model Name : " + model.model_name + ", Optimizer : differential evolution"
    frontier = build_frontier()
    e = model.eval(frontier[0])
    best_sol = frontier[0]

    k_max = 1000
    k = 0
    cf = 0.3
    threshold = 0

    while k < k_max:
        output = ""
        
        if model.normalize_val(e) == threshold:
            break

        for i, solution in enumerate(frontier):
            seen = get_frontier_neighbors(i)
            mutation = frontier[seen[0]]
            cur_e = model.eval(solution)
            out = "."
            if cf < random.random():
                if model.eval(mutation) < cur_e:
                    cur_e = model.eval(mutation)
                    frontier[i] = mutation
                    out += "+"
            else:
                mutation = get_mutation(seen)
                if model.okay(mutation) and model.eval(mutation) < cur_e:
                    frontier[i] = mutation
                    cur_e = model.eval(mutation)
                    out = "+"
                        
            if cur_e < e and model.normalize_val(cur_e) >= threshold:
                out = "?"
                e = cur_e
                best_sol = frontier[i]
                
            output += out
            k += 1
            if k % 25 is 0:
                print ("%.5f,  %20s" % (model.normalize_val(e), output))
                output = ""

    print("\nBest Solution : " + str(best_sol))
    print("Best Energy : " + str(model.normalize_val(model.eval(best_sol))))


if __name__ == '__main__':
    differential_evolution(Golinski())
