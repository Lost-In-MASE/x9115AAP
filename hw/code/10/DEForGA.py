from __future__ import division

import random
from sk import a12

class BaseModel:

    def __init__(self):
        self.model_name = None
        self.constraints = None
        self.number_vars = 0
        self.var_bounds = []

    def okay(self, _):
        return True

    def get_neighbor(self):
        # Generate your GA variables here within bounds
        x = list()
        for i, j in self.var_bounds:
            if isinstance(i, int) and isinstance(j, int):
                x.append(random.randrange(i, j))
            else:
                x.append(random.uniform(i, j))

        return x

    def eval(self, x):
        energy = 0
        for obj in self.get_objectives():
            energy += obj(x)

        return energy

    def get_baselines(self):
        return self.lo, self.hi


class ParameterModel(BaseModel):

    def __init__(self, num_dec, num_obj):
        BaseModel.__init__(self)
        self.model_name = "ParameterModel"
        self.number_vars = num_dec
        self.number_obj = num_obj
        self.var_bounds = []
        for _ in xrange(self.number_vars):
            self.var_bounds.append((0.0, 1.0))

    def eval(self, x):
        # Call GA here
        mnop = 10

    def okay(self, x):
        for constraint in self.constraints:
            if constraint(x) < 0:
                return False

        return True


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
            l, m = model.var_bounds[j]
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

def genetic_algorithm(model, mutation = 0.05, crossover = 0.80, population = 100, get_pop_flag = False):
    population_size = population
    mutate_prob = mutation
    cross_prob = crossover
    k_max = 1000
    generations = []

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
        better = any([x > y for x,y in zip(cobj1, cobj2)])
        worse = any([x < y for x,y in zip(cobj1, cobj2)])
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
    generations.append(population)
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
            if energy1 > min_sol:
                min_sol = energy1

            if energy2 > min_sol:
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
            # print "Best Energy: ", best_sol, " | Average Energy: ", best_avg_sol
            break

        population = next_gen
        generations.append(population)
        avg_energy.append(k/population_size)

        if(k/population_size > best_avg_sol):
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

    '''Calulate hyper volume'''
    hv = cal_hv(model, generations, population_size)
    print("Hyper Volume: ", hv)
    if not get_pop_flag:
        return hv
    else:
        return population
    # print "Best Energy: ", best_sol, " | Average Energy: ", best_avg_sol, "Length of Population: "
    # return population
    # print avg_energy

def cal_hv(model, generations, population_size):
    threshold = 100000
    total_gen = len(generations)

    frontier = generations[total_gen - 1]

    for _ in xrange(threshold):
        gen_index = random.randint(0, total_gen - 2)
        front_index = random.randint(0, len(frontier) - 1)
        pop_index = random.randint(0, population_size - 1)

        frontier_can = frontier[front_index]
        can = generations[gen_index][pop_index]
        if model.type1(frontier_can, can):
            continue
        elif model.type1(can, frontier_can):
            frontier[front_index] = can
            generations[gen_index][pop_index] = frontier_can
        else :
            frontier.append(can)

    for can1 in frontier:
        for can2 in frontier:
            if can1 == can2:
                continue
            if model.type1(can1, can2):
                frontier.remove(can2)

    hv = (total_gen * population_size - len(frontier)) / (total_gen * population_size)
    return hv