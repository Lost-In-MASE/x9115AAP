from __future__ import division
from random import randrange
from random import randint
from random import random


var_bound_top = [10, 10, 5, 6, 5, 10]
var_bound_bottom = [0, 0, 1, 0, 1, 0]
steps = 10


def constraints(x):
    constraint = list()
    constraint.append(x[0] + x[1] - 2)
    constraint.append(6 - x[0] - x[1])
    constraint.append(2 - x[1] + x[0])
    constraint.append(2 - x[0] + 3*x[1])
    constraint.append(4 - x[3] - (x[2] - 3)**2)
    constraint.append((x[4] - 3)**3 + x[5] - 4)
    for c in constraint:
        if c < 0:
            return False

    return True


def get_random_assignments():
    while True:
        x = list()
        for i, j in zip(var_bound_top, var_bound_bottom):
            x.append(randrange(j, i))

        if constraints(x):
            return x


def osyczka(x):
    f1 = -(25 * (x[0] - 2)**2 + (x[1] - 2)**2 + (x[2] - 1)**2 * (x[3] - 4)**2 + (x[4] - 1)**2)
    f2 = sum([i**2 for i in x])
    return f1 + f2


def change_to_maximize(soln, index):
    evals = 0
    best = soln
    solution = soln
    delta = (var_bound_top[index] - var_bound_bottom[index])/steps
    for i in xrange(0, steps):
        evals += 1
        solution[index] = var_bound_bottom[index] + delta*i
        if constraints(solution) and osyczka(solution) > osyczka(best):
            best = list(solution)
    return best, evals


def max_walk_sat():
    max_tries = 100
    max_changes = 50
    p = 0.5
    threshold = 200

    evals = 0
    init_soln = get_random_assignments()

    for i in range(0, max_tries):
        output = str()
        new_soln = get_random_assignments()

        for j in range(0, max_changes):
            result = str()
            if osyczka(new_soln) > threshold:
                return new_soln

            c = randint(0, 5)
            if p < random():
                copy_list = list(new_soln)
                copy_list[c] = randrange(var_bound_bottom[c], var_bound_top[c])

                if constraints(copy_list):
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
            if osyczka(new_soln) > osyczka(init_soln):
                init_soln = list(new_soln)

        print "Evals : " + str(evals) + " Current Best Energy : " + str(osyczka(init_soln)) + " " + output
    return init_soln


if __name__ == '__main__':
    best_solution = max_walk_sat()
    best_energy = osyczka(best_solution)
    print("\nBest Solution : " + str(best_solution))
    print("Best Energy : " + str(best_energy))
