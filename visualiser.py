import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def build_fig(Config):

    fig = plt.figure(figsize=(5,7))
    spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[5,2])

    ax1 = fig.add_subplot(spec[0,0])

    ax2 = fig.add_subplot(spec[1,0])
    

    return fig, spec, ax1, ax2


def draw_tstep(Config, population, pop_tracker, frame,fig, spec, ax1, ax2):
  
    palette = Config.palettes

    spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[5,2])
    ax1.clear()
    ax2.clear()
    
    ax1.axvline(x=Config.world_size[0]/3,color='black')
    ax1.axvline(x=2*Config.world_size[0]/3,color='black')
    ax1.axhline(y=Config.world_size[1]/2,color='black')

    ax1.set_xlim(Config.xbounds[0], Config.xbounds[1])
    ax1.set_ylim(Config.ybounds[0], Config.ybounds[1])


    healthy = population[population[:,6] == 0][:,1:3]
    ax1.scatter(healthy[:,0], healthy[:,1], color=palette[0], s = 20, label='healthy')
    
    infected = population[population[:,6] == 1][:,1:3]
    ax1.scatter(infected[:,0], infected[:,1], color=palette[1], s = 20, label='infected')

    immune = population[population[:,6] == 2][:,1:3]
    ax1.scatter(immune[:,0], immune[:,1], color=palette[2], s = 20, label='immune')
    
    fatalities = population[population[:,6] == 3][:,1:3]
    ax1.scatter(fatalities[:,0], fatalities[:,1], color=palette[3], s = 20, label='dead')
        
    ax1.text(Config.xbounds[0], Config.ybounds[1] + ((Config.ybounds[1] - Config.ybounds[0]) / 100), 'timestep: %i, total: %i, healthy: %i infected: %i immune: %i fatalities: %i' %(frame, len(population), len(healthy), len(infected), len(immune), len(fatalities)), fontsize=10)
    
    ax2.set_title('number of infected')

    ax2.set_ylim(0, Config.pop_size + 200)

    
    ax2.plot(pop_tracker.susceptible, color=palette[0], label='susceptible')
    ax2.plot(pop_tracker.infectious, color=palette[1], label='infectious')
    ax2.plot(pop_tracker.recovered, color=palette[2], label='recovered')
    ax2.plot(pop_tracker.fatalities, color=palette[3], label='fatalities')

    ax2.legend(loc = 'best', fontsize = 6)
    
    plt.draw()
    plt.pause(0.0001)
       
            

