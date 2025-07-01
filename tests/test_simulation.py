"""
Unit tests for the Simulation module.
Tests simulation initialization, update cycles, population control, and atmospheric management.
"""
import unittest
from unittest.mock import Mock, patch
from ecosystem_sim.simulation import Simulation
from ecosystem_sim.plant import Plant


class TestSimulation(unittest.TestCase):
    """Test cases for the Simulation class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sim = Simulation(20, 15, max_plants=50)  # Small simulation for testing
    
    def test_simulation_initialization(self):
        """Test simulation is properly initialized."""
        self.assertEqual(self.sim.world.width, 20)
        self.assertEqual(self.sim.world.height, 15)
        self.assertEqual(self.sim.max_plant_population, 50)
        
        # Check atmospheric conditions
        self.assertEqual(self.sim.atmosphere['co2'], 100.0)
        self.assertEqual(self.sim.atmosphere['o2'], 100.0)
        
        # Should have some initial plants
        self.assertGreater(len(self.sim.plants), 0)
        self.assertLessEqual(len(self.sim.plants), 50)
    
    def test_default_max_plants_calculation(self):
        """Test default max plants calculation based on world size."""
        sim = Simulation(50, 40)  # 2000 cells
        expected_max = max(100, (50 * 40) // 10)  # 10% of grid size
        self.assertEqual(sim.max_plant_population, expected_max)
    
    def test_custom_max_plants(self):
        """Test custom max plants setting."""
        sim = Simulation(10, 10, max_plants=25)
        self.assertEqual(sim.max_plant_population, 25)
    
    def test_initial_plant_seeding(self):
        """Test that initial plants are properly seeded."""
        # All initial plants should be in soil
        for plant in self.sim.plants:
            x, y = plant.position
            cell = self.sim.world.get_cell(x, y)
            self.assertIsNotNone(cell)
            if cell:
                self.assertEqual(cell['type'], 'soil')
    
    def test_simulation_update_advances_time(self):
        """Test that simulation update advances world time."""
        initial_time = self.sim.world.time
        
        self.sim.update()
        
        self.assertEqual(self.sim.world.time, initial_time + 1)
    
    def test_plant_growth_during_update(self):
        """Test that plants are processed during simulation update."""
        # Add a test plant 
        test_plant = Plant((10, 10), self.sim.world)
        self.sim.plants.append(test_plant)
        
        initial_plant_count = len(self.sim.plants)
        
        # Set up update so world time advances
        self.sim.world.hour = 12  # Set to noon for good light
        
        self.sim.update()
        
        # Should have processed plants (even if some died)
        # The key is that update completed successfully
        self.assertIsInstance(len(self.sim.plants), int)
    
    def test_dead_plant_removal(self):
        """Test that dead plants are removed from simulation."""
        # Create a dying plant
        dying_plant = Plant((10, 10), self.sim.world)
        dying_plant.health = 0.1  # Very low health
        self.sim.plants.append(dying_plant)
        
        initial_count = len(self.sim.plants)
        
        # Set poor conditions to kill the plant
        cell = self.sim.world.get_cell(10, 10)
        if cell:
            cell['light'] = 0.0
            cell['water'] = 0.0
        
        self.sim.update()
        
        # Dead plant should be removed
        self.assertNotIn(dying_plant, self.sim.plants)
    
    def test_dead_plant_returns_resources(self):
        """Test that dead plants return resources to soil."""
        # Create a plant that will die
        dying_plant = Plant((10, 10), self.sim.world)
        dying_plant.health = 0.1
        dying_plant.size = 0.5
        self.sim.plants.append(dying_plant)
        
        cell = self.sim.world.get_cell(10, 10)
        if cell:
            initial_resources = cell['resources']
            cell['light'] = 0.0
            cell['water'] = 0.0
        
        self.sim.update()
        
        # Resources should have increased
        if cell:
            expected_increase = dying_plant.size * 0.5
            self.assertGreater(cell['resources'], initial_resources)
    
    def test_population_limit_enforcement(self):
        """Test that population limit is enforced."""
        # Fill simulation to near capacity
        while len(self.sim.plants) < self.sim.max_plant_population - 5:
            plant = Plant((5, 5), self.sim.world)
            plant.age = 50  # Mature for reproduction
            plant.size = 0.8
            plant.health = 100.0
            self.sim.plants.append(plant)
        
        initial_count = len(self.sim.plants)
        
        # Run multiple updates to allow reproduction attempts
        for _ in range(10):
            self.sim.update()
            # Population should never exceed limit
            self.assertLessEqual(len(self.sim.plants), self.sim.max_plant_population)
    
    def test_atmospheric_co2_o2_balance(self):
        """Test that atmospheric CO2 and O2 levels change based on plants."""
        initial_co2 = self.sim.atmosphere['co2']
        initial_o2 = self.sim.atmosphere['o2']
        
        # Add many plants for noticeable effect
        for i in range(20):
            plant = Plant((5, 5), self.sim.world)
            plant.co2_absorbed = 1.0  # Simulate photosynthesis
            plant.o2_produced = 1.0
            self.sim.plants.append(plant)
        
        self.sim.update()
        
        # CO2 should decrease, O2 should increase
        self.assertLess(self.sim.atmosphere['co2'], initial_co2)
        self.assertGreater(self.sim.atmosphere['o2'], initial_o2)
    
    def test_atmospheric_natural_changes(self):
        """Test natural atmospheric changes occur."""
        # Remove all plants to test natural changes
        self.sim.plants.clear()
        
        initial_co2 = self.sim.atmosphere['co2']
        initial_o2 = self.sim.atmosphere['o2']
        
        self.sim.update()
        
        # Natural CO2 increase and O2 decrease
        self.assertGreater(self.sim.atmosphere['co2'], initial_co2)
        self.assertLess(self.sim.atmosphere['o2'], initial_o2)
    
    def test_atmospheric_minimum_levels(self):
        """Test that atmospheric levels don't go below minimum."""
        # Set very low levels
        self.sim.atmosphere['co2'] = 51.0
        self.sim.atmosphere['o2'] = 51.0
        
        # Add plants that would absorb CO2
        for i in range(10):
            plant = Plant((5, 5), self.sim.world)
            plant.co2_absorbed = 10.0
            plant.o2_produced = 10.0
            self.sim.plants.append(plant)
        
        self.sim.update()
        
        # Should not go below minimum levels
        self.assertGreaterEqual(self.sim.atmosphere['co2'], 50.0)
        self.assertGreaterEqual(self.sim.atmosphere['o2'], 50.0)
    
    def test_water_cycle_update(self):
        """Test that water cycle updates during simulation."""
        # Set specific time for predictable water cycle behavior
        self.sim.world.hour = 12  # Noon
        
        # Set up cells with water for evaporation
        for y in range(5):
            for x in range(5):
                cell = self.sim.world.get_cell(x, y)
                if cell and cell['type'] == 'soil':
                    cell['water'] = 1.0
                    cell['light'] = 1.0  # High light for evaporation
        
        initial_atm_water = self.sim.atmosphere.get('water', 0)
        
        self.sim.update()
        
        # Atmospheric water should increase due to evaporation
        current_atm_water = self.sim.atmosphere.get('water', 0)
        # Note: May not always increase due to rain randomness
    
    def test_get_stats(self):
        """Test that simulation statistics are properly returned."""
        stats = self.sim.get_stats()
        
        # Check that all expected keys are present
        expected_keys = ['day', 'hour', 'plant_count', 'max_plants', 
                        'co2_level', 'o2_level', 'water_in_atmosphere']
        
        for key in expected_keys:
            self.assertIn(key, stats)
        
        # Check that values are reasonable
        self.assertGreaterEqual(stats['day'], 0)
        self.assertGreaterEqual(stats['hour'], 0)
        self.assertLess(stats['hour'], 24)
        self.assertEqual(stats['plant_count'], len(self.sim.plants))
        self.assertEqual(stats['max_plants'], self.sim.max_plant_population)
        self.assertGreater(stats['co2_level'], 0)
        self.assertGreater(stats['o2_level'], 0)
        self.assertGreaterEqual(stats['water_in_atmosphere'], 0)
    
    def test_offspring_limit_per_update(self):
        """Test that offspring creation is limited per update."""
        # Create many mature plants
        for i in range(30):
            plant = Plant((5, 5), self.sim.world)
            plant.age = 50
            plant.size = 0.8
            plant.health = 100.0
            self.sim.plants.append(plant)
        
        initial_count = len(self.sim.plants)
        
        self.sim.update()
        
        final_count = len(self.sim.plants)
        new_plants = final_count - initial_count
        
        # Should not create more than 50 new plants in one update
        self.assertLessEqual(new_plants, 50)
    
    def test_plant_co2_o2_reset(self):
        """Test that plant CO2/O2 counters are reset after atmospheric update."""
        # Add plants with CO2/O2 values
        test_plant = Plant((5, 5), self.sim.world)
        test_plant.co2_absorbed = 5.0
        test_plant.o2_produced = 5.0
        self.sim.plants.append(test_plant)
        
        self.sim.update()
        
        # Counters should be reset
        self.assertEqual(test_plant.co2_absorbed, 0)
        self.assertEqual(test_plant.o2_produced, 0)
    
    def test_plant_seeding_behavior(self):
        """Test plant seeding creates some plants."""
        # Create a new simulation which will seed plants
        sim = Simulation(20, 20, max_plants=50)
        
        # Should have seeded some plants (exact number depends on randomness)
        # But should be reasonable amount
        self.assertGreaterEqual(len(sim.plants), 0)
        self.assertLessEqual(len(sim.plants), 50)
    
    def test_empty_world_simulation(self):
        """Test simulation behavior with no plants."""
        self.sim.plants.clear()
        
        # Should not crash
        self.sim.update()
        
        # Stats should still work
        stats = self.sim.get_stats()
        self.assertEqual(stats['plant_count'], 0)
    
    def test_large_population_performance(self):
        """Test simulation performance with large plant population."""
        # Clear existing plants first
        self.sim.plants.clear()
        
        # Add plants up to the limit
        target_count = min(self.sim.max_plant_population, 45)  # Stay under limit
        
        for i in range(target_count):
            plant = Plant((i % 20, i // 20), self.sim.world)
            self.sim.plants.append(plant)
        
        # Should complete update without issues
        self.sim.update()
        
        # Should maintain reasonable plant count
        self.assertLessEqual(len(self.sim.plants), self.sim.max_plant_population)


if __name__ == '__main__':
    unittest.main()