"""
World module for the ecosystem simulation.
Represents the grid-based environment with various properties.
"""
import math
import random

class World:
    """
    Represents the world grid for the ecosystem simulation.
    
    Attributes:
        width (int): Width of the world grid.
        height (int): Height of the world grid.
        grid (list): 2D list of cells, each with environmental properties.
    """
    def __init__(self, width=50, height=50):
        """
        Initialize a new world with the given dimensions.
        
        Args:
            width (int): Width of the world grid.
            height (int): Height of the world grid.
        """
        self.width = width
        self.height = height
        self.time = 0
        self.hour = 0
        self.day = 0
        
        # Initialize the world grid with default soil tiles
        self.grid = []
        for y in range(height):
            row = []
            for x in range(width):
                # Default properties for each cell
                cell = {
                    'type': 'soil',
                    'light': 0.0,
                    'water': 0.7,  # Start with more water in soil
                    'temperature': 20.0,
                    'resources': 1.0
                }
                row.append(cell)
            self.grid.append(row)
        
        # Add some water bodies
        self._add_water_bodies()
    
    def _add_water_bodies(self):
        """Create some water bodies in the world."""
        # Simple lake in the middle
        lake_center_x = self.width // 2
        lake_center_y = self.height // 2
        lake_radius = min(self.width, self.height) // 8
        
        for y in range(self.height):
            for x in range(self.width):
                # Simple distance check for circular lake
                if math.sqrt((x - lake_center_x)**2 + (y - lake_center_y)**2) < lake_radius:
                    self.grid[y][x]['type'] = 'water'
                    self.grid[y][x]['water'] = 1.0
    
    def update_lighting(self, time_of_day):
        """
        Update lighting based on time of day (0-24).
        
        Args:
            time_of_day (float): Current hour of the day.
        """
        # Simplified daylight calculation
        light_level = max(0, math.sin((time_of_day / 24) * math.pi * 2))
        
        # Update lighting for all cells
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x]['light'] = light_level
    
    def get_cell(self, x, y):
        """
        Get the cell at the specified coordinates.
        
        Args:
            x (int): X coordinate.
            y (int): Y coordinate.
            
        Returns:
            dict: Cell data at the specified coordinates.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def advance_time(self):
        """
        Advance the simulation time by one hour.
        Updates lighting and other time-dependent properties.
        """
        self.time += 1
        self.hour = (self.hour + 1) % 24
        if self.hour == 0:
            self.day += 1
            
        # Update lighting based on new time
        self.update_lighting(self.hour)
