__author__ = 'abhishekravi'

from __future__ import division

import random
import math
import sys


class Individual:
    def __init__(self, decs, score):
        self.decs = decs
        self.score = score

    def compute_score(self, fitness_func):
        '''This function computes the score of the individual'''
        print "Compute score"
        return 1


def mydefault():
    print "This is a default fitness function"

class Population:
    def __init(self, pop_num = 1000,
               fitness_func = mydefault, probability = 0.05):

        self.pop_num = pop_num
        self.fitness_func = fitness_func
        self.probability = probability

    def select(self):
        '''Selection function for the Genetic Algorithm
        Tournament selection is the default implementation'''



    def crossover(self):
        '''Crossover decisions of parent individuals to get an offspring'''


    def mutate(self):
        '''Mutate a random decision of a single parent to get an offspring'''
