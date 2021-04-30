import os
import sys

import numpy as np

from config import Configuration
from infection import infect, recover_or_die
from motion import update_positions, out_of_bounds, update_randoms
from population import initialize_population, Population_trackers
from visualiser import build_fig, draw_tstep

class Simulation():
    def __init__(self):

        self.Config = Configuration()
        self.frame = 0

        self.population = initialize_population(self.Config, self.Config.xbounds, self.Config.ybounds)

        self.pop_tracker = Population_trackers()   

        self.peak_infections = 0

    def tstep(self):

        if self.frame == 0:
            self.fig, self.spec, self.ax1, self.ax2 = build_fig(self.Config)

        xbounds = np.array([[self.Config.xbounds[0] + 0.02, self.Config.xbounds[1] - 0.02]] * self.Config.pop_size)
        ybounds = np.array([[self.Config.ybounds[0] + 0.02, self.Config.ybounds[1] - 0.02]] * self.Config.pop_size)
        self.population = out_of_bounds(self.population, xbounds, ybounds)

        if self.Config.is_lockdown and self.Config.lockdown == False:
            if len(self.population[(self.population[:,6] == 1)]) >= self.Config.lockdown_percentage*self.Config.pop_size:
                self.Config.lockdown = True
                print("\nLockdown Started")

        left_range = [self.Config.xbounds[0] + 0.02, self.Config.xbounds[1]/3 - 0.02]
        mid_range = [self.Config.xbounds[1]/3 + 0.02, 2*self.Config.xbounds[1]/3 - 0.02]
        right_range = [2*self.Config.xbounds[1]/3 + 0.02, self.Config.xbounds[1] - 0.02]

        bottom_range = [self.Config.ybounds[0] + 0.02, self.Config.ybounds[1]/2 - 0.02]
        top_range = [self.Config.ybounds[1]/2 + 0.02, self.Config.ybounds[1] - 0.02]

        left_condition = (self.population[:,1] <= self.Config.xbounds[1]/3)
        mid_condition = (self.population[:,1] > self.Config.xbounds[1]/3) & (self.population[:,1] <= 2*self.Config.xbounds[1]/3)
        right_condition = (self.population[:,1] > 2*self.Config.xbounds[1]/3)

        bottom_condition = (self.population[:,2] <= self.Config.ybounds[1]/2)
        top_condition  = (self.population[:,2] > self.Config.ybounds[1]/2)
        
        
        if self.Config.lockdown:

            x_left_bottom = np.array([left_range] * len(self.population[left_condition & bottom_condition]))
            y_left_bottom = np.array([bottom_range] * len(self.population[left_condition & bottom_condition]))
            self.population[left_condition & bottom_condition] = out_of_bounds(self.population[left_condition & bottom_condition],x_left_bottom,y_left_bottom)
            
            x_left_top = np.array([left_range] * len(self.population[left_condition & top_condition]))
            y_left_top = np.array([top_range] * len(self.population[left_condition & top_condition]))
            self.population[left_condition & top_condition] = out_of_bounds(self.population[left_condition & top_condition],x_left_top,y_left_top)
            
            x_mid_bottom = np.array([mid_range] * len(self.population[mid_condition & bottom_condition]))
            y_mid_bottom = np.array([bottom_range] * len(self.population[mid_condition & bottom_condition]))
            self.population[mid_condition & bottom_condition] = out_of_bounds(self.population[mid_condition & bottom_condition],x_mid_bottom,y_mid_bottom)
            
            x_mid_top = np.array([mid_range] * len(self.population[mid_condition & top_condition]))
            y_mid_top = np.array([top_range] * len(self.population[mid_condition & top_condition]))
            self.population[mid_condition & top_condition] = out_of_bounds(self.population[mid_condition & top_condition],x_mid_top,y_mid_top)
            
            x_right_bottom = np.array([right_range] * len(self.population[right_condition & bottom_condition]))
            y_right_bottom = np.array([bottom_range] * len(self.population[right_condition & bottom_condition]))
            self.population[right_condition & bottom_condition] = out_of_bounds(self.population[right_condition & bottom_condition],x_right_bottom,y_right_bottom)
            
            x_right_top = np.array([right_range] * len(self.population[right_condition & top_condition]))
            y_right_top = np.array([top_range] * len(self.population[right_condition & top_condition]))
            self.population[right_condition & top_condition] = out_of_bounds(self.population[right_condition & top_condition],x_right_top,y_right_top)
            

        self.population = update_randoms(self.population, self.Config.pop_size, self.Config.speed)

        self.population[:,5][self.population[:,6] == 3] = 0
        
        self.population = update_positions(self.population)

        self.population = infect(self.population, self.Config, self.frame)

        self.population = recover_or_die(self.population, self.frame, self.Config)

        self.pop_tracker.update_counts(self.population)

        draw_tstep(self.Config, self.population, self.pop_tracker, self.frame, self.fig, self.spec, self.ax1, self.ax2)

        self.peak_infections = max(self.peak_infections , len(self.population[self.population[:,6] == 1]))

        if self.frame == 50:
            print('\ninfecting patient zero')
            self.population[0][6] = 1

        self.frame += 1
    

    def run(self):

        i = 0
        
        while i < 10000:
            try:
                self.tstep()
            except KeyboardInterrupt:
                print('\nCTRL-C caught, exiting')
                sys.exit(1)

            if self.frame >= 500:
                if len(self.population[(self.population[:,6] == 1) | (self.population[:,6] == 4)]) == 0:
                    break
        i = i + 1

        print('\n-----stopping-----\n')
        print('total timesteps taken: %i' %self.frame)
        print('total dead: %i' %len(self.population[self.population[:,6] == 3]))
        print('total recovered: %i' %len(self.population[self.population[:,6] == 2]))
        print('total unaffected: %i' %len(self.population[self.population[:,6] == 0]))
        print('peak infections: %i' %self.peak_infections)
        


sim = Simulation()

sim.run()
