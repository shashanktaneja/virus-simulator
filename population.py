from glob import glob
import os

import numpy as np


def initialize_population(Config,xbounds=[0, 1], ybounds=[0, 1]):
    '''

    0 : ID
    1 : x coordinate
    2 : y coordinate
    3 : x direction
    4 : y direction
    5 : speed
    6 : state (0=healthy, 1=sick, 2=immune, 3=dead)
    7 : infected_since
    8 : recovery

    '''

    population = np.zeros((Config.pop_size, 9))

    population[:,0] = [x for x in range(Config.pop_size)]

    population[:,1] = np.random.uniform(low = xbounds[0] + 0.05, high = xbounds[1] - 0.05, size = (Config.pop_size,))
    population[:,2] = np.random.uniform(low = ybounds[0] + 0.05, high = ybounds[1] - 0.05, size=(Config.pop_size,))

    population[:,3] = np.random.normal(loc = 0, scale = 1/3, size=(Config.pop_size,))
    population[:,4] = np.random.normal(loc = 0, scale = 1/3, size=(Config.pop_size,))

    population[:,5] = np.random.normal(Config.speed, Config.speed / 3)

    population[:,8] = np.random.normal(loc = 0.5, scale = 0.5 / 3, size=(Config.pop_size,))

    return population



class Population_trackers():

    def __init__(self):
        self.susceptible = []
        self.infectious = []
        self.recovered = []
        self.fatalities = []

        self.reinfect = False 

    def update_counts(self, population):

        pop_size = population.shape[0]
        self.infectious.append(len(population[population[:,6] == 1]))
        self.recovered.append(len(population[population[:,6] == 2]))
        self.fatalities.append(len(population[population[:,6] == 3]))

        self.susceptible.append(len(population[population[:,6] == 0]))
