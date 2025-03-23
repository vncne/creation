"""
Simulation module for the ecosystem simulation.
Manages the time loop and updates all entities in the world.
"""
import random
from ecosystem_sim.world import World
from ecosystem_sim.plant import Plant

class Simulation:
    """
    Manages the ecosystem simulation.
    
    Attributes:
        world (World): The world grid for the simulation.
        plants (list): List of all plants in the simulation.
    """
    def __init__(self, width=50, height=50):
        """
        Initialize a new simulation with the given world dimensions.
        
        Args:
            width (int): Width of the world grid.
            height (int): Height of the world grid.
        """
        self.world = World(width, height)
        self.plants = []
        
        # Environmental variables
        self.atmosphere = {
            'co2': 100.0,  # Starting CO2 level
            'o2': 100.0,   # Starting O2 level
        }
        
        # Initialize with some plants
        self._seed_initial_plants()
    
    def _seed_initial_plants(self, num_plants=20):
        """
        Seed the world with initial plants.
        
        Args:
            num_plants (int): Number of initial plants to create.
        """
        for _ in range(num_plants):
            # Try to find a suitable location for a plant
            for _ in range(10):  # Try up to 10 times
                x = random.randint(0, self.world.width - 1)
                y = random.randint(0, self.world.height - 1)
                
                cell = self.world.get_cell(x, y)
                if cell and cell['type'] == 'soil':
                    self.plants.append(Plant((x, y), self.world))
                    break
    
    def update(self):
        """
        Update the simulation by one step (hour).
        Updates the world and all entities.
        """
        # Advance time in the world
        self.world.advance_time()
        
        # Update water cycle
        self._update_water_cycle()
        
        # Update plants
        new_plants = []
        plants_to_remove = []
        
        for plant in self.plants:
            # Grow the plant
            if not plant.grow():
                plants_to_remove.append(plant)
                continue
                
            # Try to reproduce
            offspring = plant.reproduce()
            new_plants.extend(offspring)
        
        # Remove dead plants
        for plant in plants_to_remove:
            self.plants.remove(plant)
            
            # Dead plants return resources to soil
            x, y = plant.position
            cell = self.world.get_cell(x, y)
            if cell:
                cell['resources'] += plant.size * 0.5
        
        # Add new plants
        self.plants.extend(new_plants)
        
        # Update atmospheric conditions
        self._update_atmosphere()
    
    def _update_water_cycle(self):
        """Update the water cycle based on time of day."""
        # Simplified water cycle
        hour = self.world.hour
        is_daytime = 6 <= hour <= 18
        
        for y in range(self.world.height):
            for x in range(self.world.width):
                cell = self.world.grid[y][x]
                
                if cell['type'] == 'water':
                    # Water evaporates during day
                    if is_daytime and cell['light'] > 0.5:
                        self.atmosphere['water'] = self.atmosphere.get('water', 0) + 0.01
                
                elif cell['type'] == 'soil':
                    # Water evaporates from soil during hot days
                    if is_daytime and cell['light'] > 0.7:
                        evaporation = min(0.01, cell['water'] * 0.05)
                        cell['water'] -= evaporation
                        self.atmosphere['water'] = self.atmosphere.get('water', 0) + evaporation
                    
                    # Random rain during night or when atmospheric water is high
                    if (not is_daytime or self.atmosphere.get('water', 0) > 2.0) and random.random() < 0.05:
                        rain_amount = min(0.2, self.atmosphere.get('water', 0) * 0.5)
                        cell['water'] = min(1.0, cell['water'] + rain_amount)
                        self.atmosphere['water'] = max(0, self.atmosphere.get('water', 0) - rain_amount)
    
    def _update_atmosphere(self):
        """Update atmospheric conditions based on plants and time."""
        # Simplified atmospheric update
        total_co2_absorbed = sum(plant.co2_absorbed for plant in self.plants)
        total_o2_produced = sum(plant.o2_produced for plant in self.plants)
        
        # Reset plant counters
        for plant in self.plants:
            plant.co2_absorbed = 0
            plant.o2_produced = 0
        
        # Update atmospheric levels
        self.atmosphere['co2'] = max(50.0, self.atmosphere['co2'] - total_co2_absorbed + 0.1)  # Natural CO2 increase
        self.atmosphere['o2'] = max(50.0, self.atmosphere['o2'] + total_o2_produced - 0.1)  # Natural O2 decrease
    
    def get_stats(self):
        """
        Get current simulation statistics.
        
        Returns:
            dict: Dictionary of current simulation statistics.
        """
        return {
            'day': self.world.day,
            'hour': self.world.hour,
            'plant_count': len(self.plants),
            'co2_level': self.atmosphere['co2'],
            'o2_level': self.atmosphere['o2'],
            'water_in_atmosphere': self.atmosphere.get('water', 0),
        }
