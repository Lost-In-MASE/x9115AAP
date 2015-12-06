from __future__ import division

import random
import math
import sys

from sk import a12
from sk import rdivDemo

import math
PI = math.pi
def loss1(i,x,y):
    return (x - y) if better(i) == lt else (y - x)

def expLoss(i,x,y,n):
    return math.exp( loss1(i,x,y) / n)

def loss(x1, y1):
    x,y    = objs(x1), objs(y1)
    n      = min(len(x), len(y)) #lengths should be equal
    losses = [ expLoss(i,xi,yi,n)
                 for i, (xi, yi)
                   in enumerate(zip(x,y)) ]
    # print losses
    return sum(losses) / n

def cdom(x, y):
   "x dominates y if it losses least"
   return loss(x,y) < loss(y,x)

def gt(x,y): return x > y
def lt(x,y): return x < y

def better(i):  return lt

def f_one(x):
    return x[0]

def f_two(x):
    f1 = f_one(x)
    f2 = (1+g(x))*h(f1,g(x),2)
    return f2

def g(x):
    res = sum(x)
    res = 1 + (9/len(x))*res
    return res

def h(f1,g,M):
    theeta = 3*PI*f1
    res = (f1/(1+g))*(1+math.sin(theeta))
    res = M - res
    return res

def objs(can):
    return [f_one(can),f_two(can)]

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
        
    def type1(self, solution, sb):
        return cdom(solution, sb) #and model.eval(solution) < model.eval(sb)

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
        
    def eval(self, x):
        energy = 0
        for obj in self.get_objectives():
            energy += obj(x)

        return energy

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

    print "Model Name : " + model.model_name + ", Optimizer : simulated annealing"
    
    # Base variables
    kMax = 10**5
    eMax = 0
    output = ""

    # Start with a random value
    start_val = model.get_neighbor()
    cur_energy = model.normalize_val(model.eval(start_val))
    
    eras = 10
    previous_era = []
    current_era = []
    era_length = 100

    best_energy = cur_energy
    best_val = start_val
    cur_val = start_val
    i = 1
    while i < kMax - 1 and cur_energy > eMax:
        mutated_neighbor = model.get_neighbor()
        while model.okay(mutated_neighbor) is False:
            mutated_neighbor = model.get_neighbor()
        
        neighbor_energy = model.normalize_val(model.eval(mutated_neighbor))

        if model.type1(mutated_neighbor, best_val):
            best_energy = neighbor_energy
            best_val = mutated_neighbor
            output += "!"

        if model.type1(mutated_neighbor, cur_val):
            cur_energy = neighbor_energy
            cur_val = mutated_neighbor
            output += "+"

        elif get_probability(cur_energy, neighbor_energy,  (1 - i/kMax)**4) > random.random():
            cur_val = mutated_neighbor
            cur_energy = neighbor_energy
            output += "?"
        else:
            output += "."

        if i % 25 == 0:
            # print ("%6d : %.5f,  %25s" % (i, best_energy, output))
            output = ""
            cur_energy = 1
            
        if i % 100 is 0 and i is not 0:
            if len(previous_era) is not 0:
                eras += type2(current_era, previous_era, model)
                    
            previous_era = list(current_era)
            current_era = []
        else:
            current_era.append(mutated_neighbor)
                
        if eras == 0:
            print "Early Termination " + str(i) + " : " + str(eras)
            return previous_era

        i += 1

    # print("Best Value : " + str(best_val))
    # print("Best Energy : %f" % best_energy)
    return previous_era


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
            if model.okay(solution) and model.type1(solution, best):
                best = list(solution)
        return best, evaluations
    
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

    print "Model Name : " + model.model_name + ", Optimizer : max walk sat"
    
    max_tries = 1000
    max_changes = 50
    p = 0.5
    threshold = 0
    steps = 10
    
    eras = 3
    previous_era = []
    current_era = []
    era_length = 100

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
            if model.normalize_val(model.eval(new_soln)) < threshold:
                # print("\nBest Solution : " + str(init_soln))
                # print("Best Energy : " + str(model.normalize_val(model.eval(init_soln))))
                if len(previous_era) is not 0:
                    return previous_era
                else:
                    return current_era

            c = random.randint(1, model.number_vars) - 1
            if p < random.random():
                copy_list = list(new_soln)
                i, j = model.var_bounds[c]
                if isinstance(i, int) and isinstance(j, int):
                    copy_list[c] = random.randrange(i, j)
                else:
                    copy_list[c] = random.uniform(i, j)

                if model.okay(copy_list) and model.normalize_val(model.eval(new_soln)) >= threshold:
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
            if model.type1(new_soln, init_soln) and model.normalize_val(model.eval(new_soln)) >= threshold:
                init_soln = list(new_soln)

        # print "Evals : " + str(evals) + " Current Best Energy : " + \
        #       str(model.normalize_val(model.eval(init_soln))) + " " + output
              
        if i % 100 is 0 and i is not 0:
            if len(previous_era) is not 0:
                eras += type2(current_era, previous_era, model)
                    
            previous_era = list(current_era)
            current_era = []
        else:
            current_era.append(new_soln)
                
        if eras <= 0:
            print "Early Termination " + str(i) + " : " + str(eras)
            return previous_era

    # print("\nBest Solution : " + str(init_soln))
    # print("Best Energy : " + str(model.normalize_val(model.eval(init_soln))))
    if len(previous_era) is not 0:
        return previous_era
    else:
        return current_era


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


    print "Model Name : " + model.model_name + ", Optimizer : differential evolution"
    frontier = build_frontier()
    e = model.eval(frontier[0])
    best_sol = frontier[0]
    
    eras = 10
    previous_era = []
    current_era = []
    era_length = 100

    k_max = 100000
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
                if model.type1(mutation, solution):
                    cur_e = model.eval(mutation)
                    frontier[i] = mutation
                    out += "+"
            else:
                mutation = get_mutation(seen)
                if model.okay(mutation) and model.type1(mutation, solution):
                    frontier[i] = mutation
                    cur_e = model.eval(mutation)
                    out = "+"
                        
            if model.type1(solution, best_sol) and model.normalize_val(cur_e) >= threshold:
                out = "?"
                e = cur_e
                best_sol = frontier[i]
                
            output += out
            k += 1
            if k % 25 is 0:
                # print ("%.5f,  %20s" % (model.normalize_val(e), output))
                output = ""
                
            if k % 100 is 0 and k is not 0:
                if len(previous_era) is not 0:
                    eras += type2(current_era, previous_era, model)
                    
                previous_era = list(current_era)
                current_era = []
            else:
                current_era.append(solution)
                
            if eras == 0:
                print "Early Termination " + str(k) + " : " + str(eras)
                return previous_era

    # print("\nBest Solution : " + str(best_sol))
    # print("Best Energy : " + str(model.normalize_val(model.eval(best_sol))))
    return previous_era


if __name__ == '__main__':
            
    era_collection = []
    text = ["MWS", "SA", "DE"]
    ct = 0
    model = DTLZ7(10, 2)
    i = 0
    for _ in xrange(0, 20):
        i += 1
        for optimizer in [max_walk_sat, simulated_annealing, differential_evolution]:
            era_val = [model.normalize_val(model.eval(val)) for val in optimizer(model)]
            era_val.insert(0, text[ct%3] + str(i))
            era_collection.append(era_val)
            ct += 1
        
    # print era_collection
    print rdivDemo(era_collection)