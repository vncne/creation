"""
Unit tests for the World module.
Tests world grid initialization, cell operations, time management, and lighting.
"""
import unittest
import math
from ecosystem_sim.world import World


class TestWorld(unittest.TestCase):
    """Test cases for the World class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.world = World(10, 8)  # Small world for testing
    
    def test_world_initialization(self):
        """Test world is properly initialized with correct dimensions."""
        self.assertEqual(self.world.width, 10)
        self.assertEqual(self.world.height, 8)
        self.assertEqual(self.world.time, 0)
        self.assertEqual(self.world.hour, 0)
        self.assertEqual(self.world.day, 0)
        
        # Check grid dimensions
        self.assertEqual(len(self.world.grid), 8)  # height
        self.assertEqual(len(self.world.grid[0]), 10)  # width
    
    def test_grid_cell_initialization(self):
        """Test that grid cells are properly initialized."""
        for y in range(self.world.height):
            for x in range(self.world.width):
                cell = self.world.grid[y][x]
                
                # Check cell has required properties
                self.assertIn('type', cell)
                self.assertIn('light', cell)
                self.assertIn('water', cell)
                self.assertIn('temperature', cell)
                self.assertIn('resources', cell)
                
                # Check initial values are reasonable
                self.assertIn(cell['type'], ['soil', 'water'])
                self.assertGreaterEqual(cell['light'], 0.0)
                self.assertGreaterEqual(cell['water'], 0.0)
                self.assertLessEqual(cell['water'], 1.0)
                self.assertGreater(cell['temperature'], 0.0)
                self.assertGreater(cell['resources'], 0.0)
    
    def test_water_body_creation(self):
        """Test that water bodies are created in the world."""
        water_cells = []
        for y in range(self.world.height):
            for x in range(self.world.width):
                if self.world.grid[y][x]['type'] == 'water':
                    water_cells.append((x, y))
        
        # Should have some water cells
        self.assertGreater(len(water_cells), 0)
        
        # Water cells should have full water
        for x, y in water_cells:
            self.assertEqual(self.world.grid[y][x]['water'], 1.0)
    
    def test_get_cell_valid_coordinates(self):
        """Test getting cells with valid coordinates."""
        cell = self.world.get_cell(5, 3)
        self.assertIsNotNone(cell)
        self.assertIsInstance(cell, dict)
        
        # Test edge cases
        cell = self.world.get_cell(0, 0)
        self.assertIsNotNone(cell)
        
        cell = self.world.get_cell(9, 7)  # max valid coordinates
        self.assertIsNotNone(cell)
    
    def test_get_cell_invalid_coordinates(self):
        """Test getting cells with invalid coordinates returns None."""
        # Negative coordinates
        self.assertIsNone(self.world.get_cell(-1, 0))
        self.assertIsNone(self.world.get_cell(0, -1))
        
        # Out of bounds coordinates
        self.assertIsNone(self.world.get_cell(10, 0))  # width is 10, so max is 9
        self.assertIsNone(self.world.get_cell(0, 8))   # height is 8, so max is 7
        
        # Way out of bounds
        self.assertIsNone(self.world.get_cell(100, 100))
    
    def test_advance_time(self):
        """Test time advancement works correctly."""
        initial_time = self.world.time
        initial_hour = self.world.hour
        initial_day = self.world.day
        
        # Advance one hour
        self.world.advance_time()
        
        self.assertEqual(self.world.time, initial_time + 1)
        self.assertEqual(self.world.hour, (initial_hour + 1) % 24)
        
        # Test day rollover
        self.world.hour = 23  # Set to 11 PM
        self.world.advance_time()
        
        self.assertEqual(self.world.hour, 0)
        self.assertEqual(self.world.day, initial_day + 1)
    
    def test_lighting_calculation_noon(self):
        """Test lighting calculation at noon (peak sunlight)."""
        self.world.update_lighting(12)  # Noon
        
        # Check that all cells have maximum light
        for y in range(self.world.height):
            for x in range(self.world.width):
                light = self.world.grid[y][x]['light']
                self.assertAlmostEqual(light, 1.0, places=5)
    
    def test_lighting_calculation_midnight(self):
        """Test lighting calculation at midnight (no sunlight)."""
        self.world.update_lighting(0)  # Midnight
        
        # Check that all cells have no light
        for y in range(self.world.height):
            for x in range(self.world.width):
                light = self.world.grid[y][x]['light']
                self.assertAlmostEqual(light, 0.0, places=5)
    
    def test_lighting_calculation_dawn_dusk(self):
        """Test lighting calculation at dawn and dusk."""
        # Dawn (6 AM)
        self.world.update_lighting(6)
        dawn_light = self.world.grid[0][0]['light']
        
        # Dusk (6 PM)
        self.world.update_lighting(18)
        dusk_light = self.world.grid[0][0]['light']
        
        # Dawn and dusk should have same light level (symmetrical)
        self.assertAlmostEqual(dawn_light, dusk_light, places=5)
        
        # Should be between 0 and 1
        self.assertGreater(dawn_light, 0.0)
        self.assertLess(dawn_light, 1.0)
    
    def test_lighting_progression(self):
        """Test that lighting progresses correctly throughout the day."""
        light_levels = []
        
        for hour in range(24):
            self.world.update_lighting(hour)
            light_levels.append(self.world.grid[0][0]['light'])
        
        # Find maximum light level and its time
        max_light = max(light_levels)
        max_hour = light_levels.index(max_light)
        
        # Maximum should occur at noon
        self.assertEqual(max_hour, 12)
        self.assertAlmostEqual(max_light, 1.0, places=5)
        
        # Midnight should have minimum light
        self.assertAlmostEqual(light_levels[0], 0.0, places=5)
    
    def test_update_cell_water_valid(self):
        """Test updating cell water with valid coordinates."""
        x, y = 5, 3
        initial_cell = self.world.get_cell(x, y)
        self.assertIsNotNone(initial_cell)
        initial_water = initial_cell['water']
        
        # Add water
        result = self.world.update_cell_water(x, y, 0.2)
        self.assertTrue(result)
        
        new_cell = self.world.get_cell(x, y)
        self.assertIsNotNone(new_cell)
        new_water = new_cell['water']
        expected_water = min(1.0, initial_water + 0.2)
        self.assertAlmostEqual(new_water, expected_water, places=5)
    
    def test_update_cell_water_bounds(self):
        """Test water update respects bounds [0.0, 1.0]."""
        x, y = 5, 3
        
        # Test upper bound
        self.world.update_cell_water(x, y, 10.0)  # Try to add way too much
        cell = self.world.get_cell(x, y)
        self.assertIsNotNone(cell)
        water = cell['water']
        self.assertLessEqual(water, 1.0)
        
        # Test lower bound
        self.world.update_cell_water(x, y, -10.0)  # Try to remove way too much
        cell = self.world.get_cell(x, y)
        self.assertIsNotNone(cell)
        water = cell['water']
        self.assertGreaterEqual(water, 0.0)
    
    def test_update_cell_water_invalid_coordinates(self):
        """Test updating water with invalid coordinates returns False."""
        # Out of bounds
        result = self.world.update_cell_water(-1, 0, 0.1)
        self.assertFalse(result)
        
        result = self.world.update_cell_water(10, 0, 0.1)
        self.assertFalse(result)
        
        result = self.world.update_cell_water(0, 8, 0.1)
        self.assertFalse(result)
    
    def test_large_world_creation(self):
        """Test creation of a large world doesn't fail."""
        large_world = World(100, 100)
        
        self.assertEqual(large_world.width, 100)
        self.assertEqual(large_world.height, 100)
        
        # Check that all cells are initialized
        self.assertEqual(len(large_world.grid), 100)
        self.assertEqual(len(large_world.grid[0]), 100)
    
    def test_small_world_creation(self):
        """Test creation of a very small world."""
        tiny_world = World(1, 1)
        
        self.assertEqual(tiny_world.width, 1)
        self.assertEqual(tiny_world.height, 1)
        self.assertEqual(len(tiny_world.grid), 1)
        self.assertEqual(len(tiny_world.grid[0]), 1)


if __name__ == '__main__':
    unittest.main()