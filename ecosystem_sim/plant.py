"""
Plant module for the ecosystem simulation.
Represents plants that grow in soil with sunlight and water.
"""
import random

class Plant:
    """
    Represents a plant in the ecosystem.
    
    Attributes:
        position (tuple): (x, y) position in the world grid.
        age (int): Age of the plant in simulation ticks.
        health (float): Health value from 0 to 100.
        size (float): Size of the plant, affects resource consumption and visibility.
    """
    def __init__(self, position, world):
        """
        Initialize a new plant at the given position.
        
        Args:
            position (tuple): (x, y) position in the world grid.
            world (World): Reference to the world the plant exists in.
        """
        self.position = position
        self.age = 0
        self.health = 100.0
        self.size = 0.1  # Start as a small seedling
        self.world = world
        
        # Track plant's effect on the environment
        self.co2_absorbed = 0
        self.o2_produced = 0
    
    def grow(self):
        """
        Grow the plant based on environmental conditions.
        Plants need sunlight and water to grow and stay healthy.
        
        Returns:
            bool: True if the plant is still alive, False if dead.
        """
        x, y = self.position
        cell = self.world.get_cell(x, y)
        
        if cell is None or cell['type'] != 'soil':
            self.health -= 10  # Plants can only grow in soil
            return self.health > 0
        
        sunlight = cell['light']
        water = cell['water']
        
        # Basic growth formula based on sunlight and water
        growth_factor = min(sunlight, water) * 0.2  # Faster growth
        
        if growth_factor > 0:
            self.age += 1
            self.size += growth_factor * 0.1  # Faster size increase
            self.size = min(self.size, 1.0)  # Cap size at 1.0
            
            # Simulate photosynthesis (simplified)
            self.co2_absorbed += growth_factor
            self.o2_produced += growth_factor
            
            # Consume some water from the soil
            new_water = max(0, cell['water'] - growth_factor * 0.05)
            self.world.grid[y][x]['water'] = new_water
        else:
            # Plant suffers in poor conditions
            self.health -= 2
        
        # Age affects health after maturity
        if self.age > 100:
            self.health -= 0.5
        
        # Check if plant is still alive
        return self.health > 0
    
    def reproduce(self):
        """
        Attempt to reproduce and spread seeds.
        
        Returns:
            list: List of new plant objects (seeds) or empty list if no reproduction occurred.
        """
        # Only mature plants can reproduce
        if self.age < 30 or self.size < 0.3:  # Lower thresholds
            return []
        
        # Chance to reproduce based on plant health and size
        reproduction_chance = self.health / 100 * self.size  # Increased chance
        
        if random.random() < reproduction_chance:
            # Try to place a seed in a nearby cell
            new_plants = []
            
            # Check adjacent cells
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue  # Skip the current position
                    
                    new_x = self.position[0] + dx
                    new_y = self.position[1] + dy
                    
                    # Check if the position is valid and is soil
                    cell = self.world.get_cell(new_x, new_y)
                    if cell and cell['type'] == 'soil' and random.random() < 0.3:  # Higher chance
                        new_plant = Plant((new_x, new_y), self.world)
                        new_plants.append(new_plant)
                        break  # Only create one seed for now
            
            return new_plants
        
        return [] 