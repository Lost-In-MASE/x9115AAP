from __future__ import division

import random
from sk import a12
from sk import rdivDemo

from GenericExperimentsGA import DTLZ1, DTLZ3, DTLZ5, DTLZ7


class BaseModel:

    def __init__(self):
        self.model_name = None
        self.constraints = None
        self.number_vars = 0
        self.model_type = None
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
        # Return hyper volume ratio
        return 0

    def get_baselines(self):
        return self.lo, self.hi


class ParameterModel(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self.model_name = "ParameterModel"
        self.number_vars = 3
        self.var_bounds = [(0.01, 0.1), (0.6, 1.0), (30, 150)]

    def eval(self, x):
        # Call GA here
        return genetic_algorithm(self.model_type, x)


def differential_evolution(model_type):

    frontier_size = 30
    model = ParameterModel()
    model.model_type = model_type

    def build_frontier():
        new_frontier = []
        for _ in xrange(frontier_size):
            neighbor = model.get_neighbor()
            while model.okay(neighbor) is False:
                neighbor = model.get_neighbor()
            new_frontier.append(neighbor)

        return new_frontier

    def get_frontier_neighbors(cur):
        seen = []
        while len(seen) < 3:
            rand_index = random.randint(0, frontier_size - 1)
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

            if isinstance(l, int) and isinstance(m, int):
                inter = int(inter)
            if inter >= l and inter <= m:
                soln.append(inter)
            else:
                soln.append(frontier[seen[random.randint(0, 2)]][j])
        return soln

    print "Model Name : " + model.model_name + ", Optimizer : differential evolution"
    frontier = build_frontier()
    e = model.eval(frontier[0])
    best_sol = frontier[0]

    k_max = 20
    k = 0
    cf = 0.3

    while k < k_max:

        for i, solution in enumerate(frontier):
            seen = get_frontier_neighbors(i)
            mutation = frontier[seen[0]]
            cur_e = model.eval(solution)
            if cf < random.random():
                new_en = model.eval(mutation)
                if new_en > cur_e:
                    cur_e = new_en
                    frontier[i] = mutation
            else:
                mutation = get_mutation(seen)
                new_en = model.eval(mutation)
                if model.okay(mutation) and new_en > cur_e:
                    frontier[i] = mutation
                    cur_e = new_en

            if cur_e > e:
                print solution
                e = cur_e
                best_sol = frontier[i]

            k += 1

    print("\nBest Solution : " + str(best_sol))
    print("Best Energy : " + str(e))

    return best_sol


def genetic_algorithm(model, tuned_params):
    return genetic_algorithm(model, tuned_params, False)


def genetic_algorithm(model, tuned_params=None, get_pop_flag=False):
    if tuned_params is None:
        print "Using default"
        tuned_params = [0.5, 0.80, 100]
    population_size = tuned_params[2]  # population
    mutate_prob = tuned_params[0]  # mutation
    cross_prob = tuned_params[1]  # crossover
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
        if len(pool) is 0:
            # print "Length of pool is 0"
            return range(0, population_size)
        return pool

    def bdom_better(c1, c2):
        cobj1 = []
        cobj2 = []
        for objective in model.get_objectives():
            cobj1.append(objective(c1))
            cobj2.append(objective(c2))
        better = any([x > y for x, y in zip(cobj1, cobj2)])
        worse = any([x < y for x, y in zip(cobj1, cobj2)])
        return better and not worse

    print "Model Name : " + model.model_name + ", Optimizer : Genetic Algorithm"
    population = build_population()
    best_sol = model.normalize_val(model.eval(population[0]))
    sumofpop = 0
    for i in population:
        sumofpop += model.eval(i)
    best_avg_sol = sumofpop / population_size
    avg_energy = list()
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

        if k/population_size > best_avg_sol:
            best_avg_sol = k/population_size

        energies = []
        for i in xrange(population_size):
            # print ("%.5f \n" % (model.normalize_val(model.eval(population[i]))))
            energies.append(model.eval(population[i]))
        energies.sort()
        # print energies

        sum = 0
        # Calculate the percentage of population that are similar
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

if __name__ == '__main__':
    era_collection = []
    for model, text in zip([DTLZ1, DTLZ3, DTLZ5, DTLZ7], ["DTLZ1", "DTLZ3", "DTLZ5", "DTLZ7"]):
        for decs in [10, 20, 40]:
            for objs in [2, 4, 6, 8]:
                print "Now performing for " + text + " " + str(decs) + " " + str(objs)
                cur_model = model(decs, objs)
                era_val = []
                era_val.append(genetic_algorithm(cur_model, differential_evolution(cur_model), False))
                # era_val = [cur_model.normalize_val(cur_model.eval(val)) for val in genetic_algorithm(cur_model, differential_evolution(cur_model), True)]
                era_val.insert(0, text + "_" + str(decs) + "_" + str(objs) + "_tuned")
                era_collection.append(era_val)
                era_val = []
                era_val.append(genetic_algorithm(cur_model, None, True))
                # era_val = [cur_model.normalize_val(cur_model.eval(val)) for val in genetic_algorithm(cur_model, None, True)]
                era_val.insert(0, text + "_" + str(decs) + "_" + str(objs) + "_untuned")
                era_collection.append(era_val)

    print era_collection
    print rdivDemo(era_collection)
