from __future__ import division

import random


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