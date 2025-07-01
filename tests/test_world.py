import math

from ecosystem_sim.world import World


def test_world_initialization_dimensions():
    """World grid should match specified dimensions."""
    width, height = 10, 15
    world = World(width, height)
    assert world.width == width
    assert world.height == height
    # Grid should have `height` rows and `width` columns
    assert len(world.grid) == height
    assert all(len(row) == width for row in world.grid)


def test_world_add_water_bodies():
    """A lake should be created roughly at the centre of the world grid."""
    world = World(10, 10)
    centre_x, centre_y = world.width // 2, world.height // 2
    centre_cell = world.get_cell(centre_x, centre_y)
    assert centre_cell is not None
    assert centre_cell["type"] == "water"


def test_world_update_lighting_noon_and_midnight():
    """Lighting should peak at noon and be zero at midnight."""
    world = World(8, 8)

    # Noon (12h) -> maximum light
    world.update_lighting(12)
    noon_light_levels = {cell["light"] for row in world.grid for cell in row}
    assert len(noon_light_levels) == 1  # All cells have same lighting
    (noon_light,) = noon_light_levels
    assert math.isclose(noon_light, 1.0, rel_tol=1e-3)

    # Midnight (0h) -> zero light
    world.update_lighting(0)
    midnight_light_levels = {cell["light"] for row in world.grid for cell in row}
    (midnight_light,) = midnight_light_levels
    assert midnight_light == 0


def test_update_cell_water_bounds():
    """Water levels should be clamped between 0 and 1 inclusive."""
    world = World(4, 4)
    x, y = 0, 0

    # Attempt to drain all water
    world.update_cell_water(x, y, -10)
    cell = world.get_cell(x, y)
    assert cell is not None
    assert cell["water"] == 0

    # Attempt to flood beyond capacity
    world.update_cell_water(x, y, 10)
    cell = world.get_cell(x, y)
    assert cell is not None
    assert cell["water"] == 1.0