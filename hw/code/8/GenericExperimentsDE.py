from __future__ import division

import random
import math
import sys

from sk import a12


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
        
class DTLZ7(BaseModel):

    def __init__(self, num_dec, num_obj):
        BaseModel.__init__(self)
        self.model_name = "DTLZ7"
        self.number_vars = num_dec
        self.number_obj = num_obj
        self.var_bounds = []
        for _ in xrange(self.number_vars):
            self.var_bounds.append((0.0,1.0))
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

    print("Best Value : " + str(best_val))
    print("Best Energy : %f" % best_energy)


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
    while model.okay(init_soln) is False and model.normalize_val(model.eval(init_soln)) > threshold:
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
                if isinstance(i, int) and isinstance(j, int):
                    copy_list[c] = random.randrange(i, j)
                else:
                    copy_list[c] = random.uniform(i, j)

                if model.okay(copy_list) and model.normalize_val(model.eval(new_soln)) <= threshold:
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
            if model.eval(new_soln) > model.eval(init_soln) and model.normalize_val(model.eval(new_soln)) <= threshold:
                init_soln = list(new_soln)

        print "Evals : " + str(evals) + " Current Best Energy : " + \
              str(model.normalize_val(model.eval(init_soln))) + " " + output

    print("\nBest Solution : " + str(init_soln))
    print("Best Energy : " + str(model.normalize_val(model.eval(init_soln))))


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
    
    eras = 10
    previous_era = []
    current_era = []
    era_length = 100

    k_max = sys.maxint
    k = 0
    cf = 0.3
    threshold = 1

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
            
            if (k + 1) % 100 is 0:
                if len(previous_era) is not 0:
                    eras += type2(previous_era, current_era, model)
                    
                previous_era = list(current_era)
                current_era = []
            else:
                current_era.append(solution)
                
            if eras == 0:
                print "Early Termination " + str(k) + " : " + str(eras)
                return

    print("\nBest Solution : " + str(best_sol))
    print("Best Energy : " + str(model.normalize_val(model.eval(best_sol))))
    print("\n Eras : " + str(eras) + " : " + str(k))
    
def type1(solution, sb, model):
    if model.eval(solution) > model.eval(sb):
        return True
        
    return False
    
def type2(era_one, era_two, model):
    for objective in model.get_objectives():
        era_one_objective = []
        era_two_objective = []
        for i in xrange(0, len(era_one)):
            era_one_objective.append(objective(era_one[i]))
            era_two_objective.append(objective(era_two[i]))
        if (a12(era_one_objective, era_two_objective) > 0.56):
            return 5

    return -1


if __name__ == '__main__':
    # a = datetime.datetime.now()
    # simulated_annealing(Kursawe())
    # b = datetime.datetime.now()
    # print("# Runtime: %f" % ((b - a).microseconds/1000000))

    # a = datetime.datetime.now()
    # max_walk_sat(Kursawe())
    # b = datetime.datetime.now()
    # print("# Runtime: %f" % ((b - a).microseconds/1000000))

    # for software_model in [Schaffer, Osyczka, Kursawe, Golinski]:
    #     for optimizer in [simulated_annealing, max_walk_sat, differential_evolution]:
    #         print "\n\n------------------------------------------------------------\n\n"
    #         optimizer(software_model())
            
            
    differential_evolution(DTLZ7(10, 2))
