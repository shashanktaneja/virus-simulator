import numpy as np

def update_positions(population):

    population[:,1] = population[:,1] + (population[:,3] * population[:,5])

    population[:,2] = population[:,2] + (population [:,4] * population[:,5])

    return population


def out_of_bounds(population, xbounds, ybounds):

    shp = population[:,3][(population[:,1] <= xbounds[:,0]) & (population[:,3] < 0)].shape
    population[:,3][(population[:,1] <= xbounds[:,0]) & (population[:,3] < 0)] = np.clip(np.random.normal(loc = 0.5, scale = 0.5/3, size = shp), a_min = 0.05, a_max = 1)

    shp = population[:,3][(population[:,1] >= xbounds[:,1]) & (population[:,3] > 0)].shape
    population[:,3][(population[:,1] >= xbounds[:,1]) & (population[:,3] > 0)] = np.clip(-np.random.normal(loc = 0.5, scale = 0.5/3, size = shp), a_min = -1, a_max = -0.05)

    shp = population[:,4][(population[:,2] <= ybounds[:,0]) & (population[:,4] < 0)].shape
    population[:,4][(population[:,2] <= ybounds[:,0]) & (population[:,4] < 0)] = np.clip(np.random.normal(loc = 0.5, scale = 0.5/3, size = shp), a_min = 0.05, a_max = 1)

    shp = population[:,4][(population[:,2] >= ybounds[:,1]) & (population[:,4] > 0)].shape
    population[:,4][(population[:,2] >= ybounds[:,1]) & (population[:,4] > 0)] = np.clip(-np.random.normal(loc = 0.5, scale = 0.5/3, size = shp), a_min = -1, a_max = -0.05)

    return population


def update_randoms(population, pop_size, speed):

    update = np.random.random(size=(pop_size,))
    shp = update[update <= 0.02].shape
    population[:,3][update <= 0.02] = np.random.normal(loc = 0, scale = 1/3, size = shp)
   
    update = np.random.random(size=(pop_size,))
    shp = update[update <= 0.02].shape
    population[:,4][update <= 0.02] = np.random.normal(loc = 0, scale = 1/3, size = shp) 

    update = np.random.random(size=(pop_size,))
    shp = update[update <= 0.02].shape
    population[:,5][update <= 0.02] = np.random.normal(loc = speed, scale = speed / 3, size = shp)

    population[:,5] = np.clip(population[:,5], a_min=0.0001, a_max=0.05)
    return population


