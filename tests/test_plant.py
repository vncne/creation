"""
Unit tests for the Plant module.
Tests plant initialization, growth mechanics, reproduction, and environmental interactions.
"""
import unittest
from unittest.mock import Mock, MagicMock
from ecosystem_sim.plant import Plant
from ecosystem_sim.world import World


class TestPlant(unittest.TestCase):
    """Test cases for the Plant class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.world = World(10, 10)
        self.position = (5, 5)
        self.plant = Plant(self.position, self.world)
    
    def test_plant_initialization(self):
        """Test plant is properly initialized."""
        self.assertEqual(self.plant.position, (5, 5))
        self.assertEqual(self.plant.age, 0)
        self.assertEqual(self.plant.health, 100.0)
        self.assertEqual(self.plant.size, 0.1)
        self.assertEqual(self.plant.world, self.world)
        self.assertEqual(self.plant.co2_absorbed, 0)
        self.assertEqual(self.plant.o2_produced, 0)
    
    def test_plant_growth_with_good_conditions(self):
        """Test plant growth with optimal sunlight and water."""
        # Set up optimal conditions
        cell = self.world.get_cell(5, 5)
        if cell:
            cell['light'] = 1.0  # Full sunlight
            cell['water'] = 1.0  # Full water
            cell['type'] = 'soil'  # Ensure it's soil
        
        initial_size = self.plant.size
        initial_age = self.plant.age
        
        # Plant should grow successfully
        result = self.plant.grow()
        
        self.assertTrue(result)  # Plant should be alive
        self.assertGreater(self.plant.size, initial_size)
        self.assertEqual(self.plant.age, initial_age + 1)
        self.assertGreater(self.plant.co2_absorbed, 0)
        self.assertGreater(self.plant.o2_produced, 0)
    
    def test_plant_growth_with_poor_conditions(self):
        """Test plant growth with no light or water."""
        # Set up poor conditions
        cell = self.world.get_cell(5, 5)
        if cell:
            cell['light'] = 0.0  # No sunlight
            cell['water'] = 0.0  # No water
        
        initial_health = self.plant.health
        
        # Plant should suffer
        result = self.plant.grow()
        
        # Health should decrease due to poor conditions
        self.assertLess(self.plant.health, initial_health)
        self.assertEqual(self.plant.co2_absorbed, 0)
        self.assertEqual(self.plant.o2_produced, 0)
    
    def test_plant_growth_in_non_soil(self):
        """Test plant cannot grow in water tiles."""
        # Move plant to water cell
        water_plant = Plant((3, 3), self.world)
        
        # Find a water cell or create one
        cell = self.world.get_cell(3, 3)
        if cell:
            cell['type'] = 'water'
        
        initial_health = water_plant.health
        
        # Plant should suffer in water
        result = water_plant.grow()
        
        self.assertLess(water_plant.health, initial_health)
    
    def test_plant_death_from_low_health(self):
        """Test plant dies when health reaches zero."""
        self.plant.health = 1.0  # Very low health
        
        # Set poor conditions to reduce health further
        cell = self.world.get_cell(5, 5)
        if cell:
            cell['light'] = 0.0
            cell['water'] = 0.0
        
        result = self.plant.grow()
        
        # Plant should die
        self.assertFalse(result)
        self.assertLessEqual(self.plant.health, 0)
    
    def test_plant_aging_effects(self):
        """Test that aging affects plant health."""
        self.plant.age = 150  # Very old plant
        initial_health = self.plant.health
        
        # Set good conditions
        cell = self.world.get_cell(5, 5)
        if cell:
            cell['light'] = 1.0
            cell['water'] = 1.0
        
        self.plant.grow()
        
        # Health should decrease due to age
        self.assertLess(self.plant.health, initial_health)
    
    def test_plant_size_cap(self):
        """Test that plant size is capped at 1.0."""
        self.plant.size = 0.9  # Nearly max size
        
        # Set excellent conditions
        cell = self.world.get_cell(5, 5)
        if cell:
            cell['light'] = 1.0
            cell['water'] = 1.0
        
        # Grow multiple times
        for _ in range(10):
            if not self.plant.grow():
                break
        
        # Size should not exceed 1.0
        self.assertLessEqual(self.plant.size, 1.0)
    
    def test_water_consumption(self):
        """Test that plants consume water from soil."""
        # Set up conditions for growth
        cell = self.world.get_cell(5, 5)
        if cell:
            cell['light'] = 1.0
            initial_water = cell['water']
        
        self.plant.grow()
        
        # Water should have been consumed
        if cell:
            self.assertLessEqual(cell['water'], initial_water)
    
    def test_reproduction_immature_plant(self):
        """Test that young plants cannot reproduce."""
        self.plant.age = 10  # Too young
        self.plant.size = 0.1  # Too small
        
        offspring = self.plant.reproduce()
        
        self.assertEqual(len(offspring), 0)
    
    def test_reproduction_mature_plant(self):
        """Test that mature plants can attempt reproduction."""
        self.plant.age = 50   # Mature age
        self.plant.size = 0.5  # Good size
        self.plant.health = 100.0  # Healthy
        
        # Create multiple attempts to account for randomness
        total_offspring = 0
        for _ in range(100):  # Multiple attempts
            offspring = self.plant.reproduce()
            total_offspring += len(offspring)
        
        # Should have some reproduction success
        self.assertGreater(total_offspring, 0)
    
    def test_reproduction_creates_valid_plants(self):
        """Test that reproduction creates valid plant objects."""
        self.plant.age = 50
        self.plant.size = 0.8
        self.plant.health = 100.0
        
        # Try many times to get offspring
        for _ in range(100):
            offspring = self.plant.reproduce()
            if offspring:
                new_plant = offspring[0]
                
                # Check that new plant is properly initialized
                self.assertIsInstance(new_plant, Plant)
                self.assertEqual(new_plant.age, 0)
                self.assertEqual(new_plant.health, 100.0)
                self.assertEqual(new_plant.size, 0.1)
                self.assertEqual(new_plant.world, self.world)
                
                # Position should be adjacent to parent
                px, py = self.plant.position
                cx, cy = new_plant.position
                distance = abs(px - cx) + abs(py - cy)
                self.assertLessEqual(distance, 2)  # Adjacent or diagonal
                break
    
    def test_reproduction_requires_soil(self):
        """Test that plants only reproduce into soil cells."""
        # Create a plant surrounded by water
        self.plant.age = 50
        self.plant.size = 0.8
        self.plant.health = 100.0
        
        # Set all adjacent cells to water
        px, py = self.plant.position
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x, y = px + dx, py + dy
                cell = self.world.get_cell(x, y)
                if cell:
                    cell['type'] = 'water'
        
        # Multiple attempts should produce no offspring
        total_offspring = 0
        for _ in range(50):
            offspring = self.plant.reproduce()
            total_offspring += len(offspring)
        
        self.assertEqual(total_offspring, 0)
    
    def test_plant_at_world_edge(self):
        """Test plant behavior at world boundaries."""
        # Create plant at edge
        edge_plant = Plant((0, 0), self.world)
        edge_plant.age = 50
        edge_plant.size = 0.8
        edge_plant.health = 100.0
        
        # Should not crash when trying to reproduce at edge
        for _ in range(10):
            offspring = edge_plant.reproduce()
            # All offspring should be within world bounds
            for plant in offspring:
                x, y = plant.position
                self.assertGreaterEqual(x, 0)
                self.assertGreaterEqual(y, 0)
                self.assertLess(x, self.world.width)
                self.assertLess(y, self.world.height)
    
    def test_photosynthesis_tracking(self):
        """Test that CO2 absorption and O2 production are tracked."""
        # Set up good conditions
        cell = self.world.get_cell(5, 5)
        if cell:
            cell['light'] = 0.8
            cell['water'] = 0.8
            cell['type'] = 'soil'  # Ensure it's soil
        
        initial_co2 = self.plant.co2_absorbed
        initial_o2 = self.plant.o2_produced
        
        self.plant.grow()
        
        # Should have absorbed CO2 and produced O2
        self.assertGreater(self.plant.co2_absorbed, initial_co2)
        self.assertGreater(self.plant.o2_produced, initial_o2)
        
        # CO2 absorbed should equal O2 produced (simplified model)
        self.assertAlmostEqual(self.plant.co2_absorbed, self.plant.o2_produced, places=5)
    
    def test_plant_with_mock_world(self):
        """Test plant behavior with mocked world for edge cases."""
        mock_world = Mock()
        mock_world.get_cell.return_value = None  # No valid cell
        mock_world.update_cell_water = Mock(return_value=True)
        
        plant = Plant((0, 0), mock_world)
        
        # Plant should handle invalid cell gracefully
        result = plant.grow()
        
        # Plant should lose health and eventually die
        self.assertLess(plant.health, 100.0)


if __name__ == '__main__':
    unittest.main()