class Configuration():
    def __init__(self):
        
        self.world_size = [1, 1]
     
        self.xbounds = [0, self.world_size[0]]
        self.ybounds = [0, self.world_size[1]]
    
        self.pop_size = 200
        
        self.speed = 0.01 

        self.infection_range = 0.03
        self.infection_chance = 0.07 
        self.recovery_duration = (200, 500) 
        self.mortality_chance = 0.1 

        self.is_lockdown = True
        self.lockdown_percentage = 0.3
        self.lockdown = False

        self.palettes = ['gray', 'red', 'green', 'black']
        

    
