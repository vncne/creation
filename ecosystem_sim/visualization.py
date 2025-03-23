"""
Visualization module for the ecosystem simulation.
Provides simple text-based visualization of the world state.
"""

class AsciiVisualizer:
    """
    Visualizes the simulation using ASCII characters in the terminal.
    """
    def __init__(self, simulation):
        """
        Initialize the visualizer with a simulation reference.
        
        Args:
            simulation (Simulation): The simulation to visualize.
        """
        self.simulation = simulation
    
    def render(self):
        """
        Render the current state of the simulation to ASCII.
        
        Returns:
            str: ASCII representation of the simulation world.
        """
        world = self.simulation.world
        plants = self.simulation.plants
        
        # Create a visual grid
        grid = [[self._get_cell_char(x, y) for x in range(world.width)] for y in range(world.height)]
        
        # Add plants to the visualization
        for plant in plants:
            x, y = plant.position
            if 0 <= x < world.width and 0 <= y < world.height:
                # Represent plants differently based on size
                if plant.size < 0.3:
                    grid[y][x] = ','  # Small seedling
                elif plant.size < 0.7:
                    grid[y][x] = '*'  # Medium plant
                else:
                    grid[y][x] = '♣'  # Large plant
        
        # Convert grid to string
        rows = [''.join(row) for row in grid]
        visual = '\n'.join(rows)
        
        # Add stats
        stats = self.simulation.get_stats()
        stats_str = (
            f"Day: {stats['day']} | Hour: {stats['hour']} | Plants: {stats['plant_count']}\n"
            f"CO2: {stats['co2_level']:.1f} | O2: {stats['o2_level']:.1f} | Atm. Water: {stats['water_in_atmosphere']:.1f}"
        )
        
        return f"{stats_str}\n\n{visual}"
    
    def _get_cell_char(self, x, y):
        """
        Get the character representation for a cell.
        
        Args:
            x (int): X coordinate of the cell.
            y (int): Y coordinate of the cell.
            
        Returns:
            str: Character representation of the cell.
        """
        cell = self.simulation.world.get_cell(x, y)
        
        if cell['type'] == 'water':
            return '~'  # Water
        elif cell['type'] == 'soil':
            # Show soil moisture level
            if cell['water'] < 0.2:
                return '.'  # Dry soil
            elif cell['water'] < 0.6:
                return ':'  # Moist soil
            else:
                return '='  # Wet soil
        else:
            return ' '  # Default/air
    
    def clear_screen(self):
        """Print ANSI escape sequence to clear the screen."""
        print("\033[H\033[J", end="") 