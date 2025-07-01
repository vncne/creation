import random

from ecosystem_sim.simulation import Simulation


def test_simulation_seeds_initial_plants():
    """Simulation should start with a default seed count."""
    sim = Simulation(width=20, height=20, max_plants=200)
    # Default seed count is 20 (see _seed_initial_plants default arg)
    assert len(sim.plants) == 20


def test_simulation_update_advances_time():
    sim = Simulation(width=10, height=10, max_plants=100)
    initial_hour = sim.world.hour
    sim.update()
    assert sim.world.hour == (initial_hour + 1) % 24


def test_simulation_population_never_exceeds_limit():
    max_plants = 30
    sim = Simulation(width=10, height=10, max_plants=max_plants)

    # Encourage reproduction by maximising chances
    random.seed(0)

    for _ in range(200):
        sim.update()
        assert len(sim.plants) <= max_plants