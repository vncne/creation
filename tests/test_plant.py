import random

import pytest  # type: ignore

from ecosystem_sim.world import World
from ecosystem_sim.plant import Plant


def test_plant_grows_when_conditions_are_good():
    """Plant size should increase and remain alive under good conditions."""
    world = World(3, 3)
    # Ensure favourable conditions
    cell = world.get_cell(0, 0)
    assert cell is not None
    cell["light"] = 1.0
    cell["water"] = 1.0

    plant = Plant((0, 0), world)
    initial_size = plant.size

    alive = plant.grow()
    assert alive is True
    assert plant.size > initial_size
    # Water in the soil should decrease slightly
    cell_after = world.get_cell(0, 0)
    assert cell_after is not None
    assert cell_after["water"] < 1.0


def test_plant_dies_in_poor_conditions():
    """Plant health should deteriorate and eventually the plant should die when conditions are poor."""
    world = World(3, 3)
    cell = world.get_cell(0, 0)
    assert cell is not None
    cell["light"] = 0.0
    cell["water"] = 0.0

    plant = Plant((0, 0), world)

    # Simulate several unsuccessful growth attempts
    for _ in range(60):
        alive = plant.grow()
        if not alive:
            break

    assert alive is False
    assert plant.health <= 0


def test_plant_reproduction_monkeypatched(monkeypatch):
    """With favourable conditions and forced random values, plant should reproduce."""
    world = World(3, 3)

    # Mature and healthy plant
    plant = Plant((1, 1), world)
    plant.age = 50
    plant.size = 0.5
    plant.health = 100.0

    # All adjacent cells are soil already in default world (3x3 grid)

    # Prepare a generator to control successive random.random() outputs.
    # First call (reproduction chance) -> 0.0 (ensures reproduction)
    # Second call (cell suitability) -> 0.0 (ensures seed is placed)
    random_values = iter([0.0, 0.0])

    def fake_random():
        return next(random_values)

    monkeypatch.setattr(random, "random", fake_random)

    offspring = plant.reproduce()
    assert len(offspring) == 1
    baby = offspring[0]
    assert isinstance(baby, Plant)
    # Baby should be in one of the adjacent coordinates
    dx = abs(baby.position[0] - plant.position[0])
    dy = abs(baby.position[1] - plant.position[1])
    assert max(dx, dy) == 1 and (dx + dy) > 0