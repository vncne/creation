"""
Unit tests for the Visualization module.
Tests ASCII visualization rendering, character mapping, and display formatting.
"""
import unittest
from unittest.mock import Mock
from ecosystem_sim.visualization import AsciiVisualizer
from ecosystem_sim.simulation import Simulation
from ecosystem_sim.plant import Plant


class TestAsciiVisualizer(unittest.TestCase):
    """Test cases for the AsciiVisualizer class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sim = Simulation(10, 8, max_plants=20)  # Small simulation for testing
        self.visualizer = AsciiVisualizer(self.sim)
    
    def test_visualizer_initialization(self):
        """Test visualizer is properly initialized."""
        self.assertEqual(self.visualizer.simulation, self.sim)
    
    def test_render_returns_string(self):
        """Test that render returns a string."""
        result = self.visualizer.render()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_render_includes_stats(self):
        """Test that render includes simulation statistics."""
        result = self.visualizer.render()
        
        # Should include key statistics
        self.assertIn('Day:', result)
        self.assertIn('Hour:', result)
        self.assertIn('Plants:', result)
        self.assertIn('CO2:', result)
        self.assertIn('O2:', result)
    
    def test_render_includes_grid(self):
        """Test that render includes the world grid."""
        result = self.visualizer.render()
        
        # Split into lines
        lines = result.split('\n')
        
        # Should have statistics lines plus grid lines
        # Statistics take 2-3 lines, plus empty line, plus grid
        self.assertGreater(len(lines), 8)  # At least grid height
        
        # Grid lines should have correct width
        grid_lines = lines[3:]  # Skip stats and empty line
        for line in grid_lines[:self.sim.world.height]:
            if line.strip():  # Skip empty lines
                self.assertEqual(len(line), self.sim.world.width)
    
    def test_get_cell_char_water(self):
        """Test water cell character representation."""
        # Set up a water cell
        cell = self.sim.world.get_cell(5, 5)
        if cell:
            cell['type'] = 'water'
        
        char = self.visualizer._get_cell_char(5, 5)
        self.assertEqual(char, '~')
    
    def test_get_cell_char_dry_soil(self):
        """Test dry soil character representation."""
        cell = self.sim.world.get_cell(5, 5)
        if cell:
            cell['type'] = 'soil'
            cell['water'] = 0.1  # Dry
        
        char = self.visualizer._get_cell_char(5, 5)
        self.assertEqual(char, '.')
    
    def test_get_cell_char_moist_soil(self):
        """Test moist soil character representation."""
        cell = self.sim.world.get_cell(5, 5)
        if cell:
            cell['type'] = 'soil'
            cell['water'] = 0.4  # Moist
        
        char = self.visualizer._get_cell_char(5, 5)
        self.assertEqual(char, ':')
    
    def test_get_cell_char_wet_soil(self):
        """Test wet soil character representation."""
        cell = self.sim.world.get_cell(5, 5)
        if cell:
            cell['type'] = 'soil'
            cell['water'] = 0.8  # Wet
        
        char = self.visualizer._get_cell_char(5, 5)
        self.assertEqual(char, '=')
    
    def test_get_cell_char_unknown_type(self):
        """Test unknown cell type character representation."""
        cell = self.sim.world.get_cell(5, 5)
        if cell:
            cell['type'] = 'unknown'
        
        char = self.visualizer._get_cell_char(5, 5)
        self.assertEqual(char, ' ')
    
    def test_plant_representation_small(self):
        """Test small plant character representation."""
        # Clear existing plants
        self.sim.plants.clear()
        
        # Add a small plant
        plant = Plant((5, 5), self.sim.world)
        plant.size = 0.2  # Small
        self.sim.plants.append(plant)
        
        result = self.visualizer.render()
        lines = result.split('\n')
        
        # Find the grid and check for small plant character
        grid_found = False
        for line in lines[3:]:  # Skip stats
            if len(line) >= 6:  # Ensure line is long enough
                if ',' in line:  # Small plant character
                    grid_found = True
                    break
        
        self.assertTrue(grid_found or len(self.sim.plants) == 0)
    
    def test_plant_representation_medium(self):
        """Test medium plant character representation."""
        self.sim.plants.clear()
        
        plant = Plant((5, 5), self.sim.world)
        plant.size = 0.5  # Medium
        self.sim.plants.append(plant)
        
        result = self.visualizer.render()
        
        # Should contain medium plant character
        self.assertIn('*', result)
    
    def test_plant_representation_large(self):
        """Test large plant character representation."""
        self.sim.plants.clear()
        
        plant = Plant((5, 5), self.sim.world)
        plant.size = 0.8  # Large
        self.sim.plants.append(plant)
        
        result = self.visualizer.render()
        
        # Should contain large plant character
        self.assertIn('♣', result)
    
    def test_multiple_plants_same_cell(self):
        """Test behavior when multiple plants are in the same cell."""
        self.sim.plants.clear()
        
        # Add multiple plants at same position
        plant1 = Plant((5, 5), self.sim.world)
        plant1.size = 0.2
        plant2 = Plant((5, 5), self.sim.world)
        plant2.size = 0.8  # Larger plant
        
        self.sim.plants.extend([plant1, plant2])
        
        result = self.visualizer.render()
        
        # Last plant processed should determine the character
        # Since plant2 is larger, should show large plant character
        self.assertIn('♣', result)
    
    def test_plants_outside_bounds(self):
        """Test plants positioned outside world bounds don't crash."""
        self.sim.plants.clear()
        
        # Add plant outside bounds
        plant = Plant((20, 20), self.sim.world)  # Outside 10x8 world
        self.sim.plants.append(plant)
        
        # Should not crash
        result = self.visualizer.render()
        self.assertIsInstance(result, str)
    
    def test_stats_formatting(self):
        """Test statistics formatting in output."""
        # Set specific values for testing
        self.sim.world.day = 5
        self.sim.world.hour = 14
        self.sim.atmosphere['co2'] = 95.7
        self.sim.atmosphere['o2'] = 104.3
        self.sim.atmosphere['water'] = 2.1
        
        result = self.visualizer.render()
        
        # Check specific formatting
        self.assertIn('Day: 5', result)
        self.assertIn('Hour: 14', result)
        self.assertIn('Plants: ', result)
        self.assertIn('95.7', result)  # CO2 level
        self.assertIn('104.3', result)  # O2 level
        self.assertIn('2.1', result)  # Atmospheric water
    
    def test_empty_simulation(self):
        """Test visualization of empty simulation."""
        self.sim.plants.clear()
        
        result = self.visualizer.render()
        
        # Should show 0 plants
        self.assertIn('Plants: 0/', result)
        
        # Should still render the grid
        lines = result.split('\n')
        self.assertGreater(len(lines), 5)
    
    def test_clear_screen(self):
        """Test clear screen functionality."""
        import io
        import sys
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.visualizer.clear_screen()
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        # Check that ANSI escape sequence was printed
        output = captured_output.getvalue()
        self.assertEqual(output, "\033[H\033[J")
    
    def test_render_consistency(self):
        """Test that render produces consistent output for same state."""
        result1 = self.visualizer.render()
        result2 = self.visualizer.render()
        
        # Should be identical if simulation state hasn't changed
        self.assertEqual(result1, result2)
    
    def test_large_simulation_rendering(self):
        """Test rendering performance with larger simulation."""
        large_sim = Simulation(50, 30, max_plants=100)
        large_visualizer = AsciiVisualizer(large_sim)
        
        # Should complete without issues
        result = large_visualizer.render()
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        
        # Check grid dimensions in output
        lines = result.split('\n')
        grid_lines = [line for line in lines[3:] if len(line) >= 30]
        self.assertGreaterEqual(len(grid_lines), 25)  # Should have most of the grid
    
    def test_visualizer_with_mock_simulation(self):
        """Test visualizer with mocked simulation for edge cases."""
        mock_sim = Mock()
        mock_sim.world = Mock()
        mock_sim.world.width = 5
        mock_sim.world.height = 3
        mock_sim.plants = []
        
        # Mock get_cell to return a standard soil cell
        mock_cell = {
            'type': 'soil',
            'water': 0.5,
            'light': 0.5,
            'temperature': 20.0,
            'resources': 1.0
        }
        mock_sim.world.get_cell.return_value = mock_cell
        
        # Mock get_stats
        mock_sim.get_stats.return_value = {
            'day': 1,
            'hour': 12,
            'plant_count': 0,
            'max_plants': 10,
            'co2_level': 100.0,
            'o2_level': 100.0,
            'water_in_atmosphere': 0.0
        }
        
        visualizer = AsciiVisualizer(mock_sim)
        result = visualizer.render()
        
        self.assertIsInstance(result, str)
        self.assertIn('Day: 1', result)
        self.assertIn('Plants: 0/10', result)
    
    def test_water_level_boundaries(self):
        """Test water level boundary conditions for character mapping."""
        # Test exactly at boundaries
        test_cases = [
            (0.0, '.'),    # Exactly dry
            (0.2, ':'),    # Exactly at moist boundary
            (0.6, '='),    # Exactly at wet boundary
            (1.0, '='),    # Maximum water
        ]
        
        for water_level, expected_char in test_cases:
            cell = self.sim.world.get_cell(5, 5)
            if cell:
                cell['type'] = 'soil'
                cell['water'] = water_level
            
            char = self.visualizer._get_cell_char(5, 5)
            self.assertEqual(char, expected_char, 
                           f"Water level {water_level} should produce '{expected_char}', got '{char}'")


if __name__ == '__main__':
    unittest.main()