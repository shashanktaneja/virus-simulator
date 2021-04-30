import numpy as np

def find_nearby(population, infection_zone):

    indices = np.int32(population[:,0][(infection_zone[0] < population[:,1]) & (population[:,1] < infection_zone[2]) & (infection_zone[1] < population [:,2]) & (population[:,2] < infection_zone[3]) & (population[:,6] == 0)])
    return indices

        
def infect(population, Config, frame):

    infected = population[population[:,6] == 1]

    for patient in infected:

        infection_zone = [patient[1] - Config.infection_range, patient[2] - Config.infection_range, patient[1] + Config.infection_range, patient[2] + Config.infection_range]

        indices = find_nearby(population, infection_zone)

        for idx in indices:
            if np.random.random() < Config.infection_chance:
                population[idx][6] = 1
                population[idx][7] = frame

    return population


def recover_or_die(population, frame, Config):

    infected = population[population[:,6] == 1]

    illness_duration= frame - infected[:,7]
    
    recovery_odds = (illness_duration - Config.recovery_duration[0]) / np.ptp(Config.recovery_duration)
    recovery_odds = np.clip(recovery_odds, a_min = 0, a_max = None)

    indices = infected[:,0][recovery_odds >= infected[:,8]]

    for idx in indices:

        if np.random.random() <= Config.mortality_chance:
            infected[:,6][infected[:,0] == idx] = 3
        else:
            infected[:,6][infected[:,0] == idx] = 2


    population[population[:,6] == 1] = infected

    return population

