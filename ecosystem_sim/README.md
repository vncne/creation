# Ecosystem Simulation

A simple ecosystem simulation that models a self-sustaining world with plants, water cycle, and atmospheric conditions.

## Features

- 2D grid-based world with soil and water tiles
- Day/night cycle with sunlight simulation
- Plants that grow, reproduce, and interact with the environment
- Water cycle (evaporation, rain)
- Atmospheric gas exchange (CO2/O2)
- Text-based visualization

## Requirements

- Python 3.6 or higher

## Installation

### From Source

```bash
# Clone or download the repository
# Navigate to the ecosystem_sim directory
cd ecosystem_sim

# Install in development mode
pip install -e .
```

## How to Run

After installation:

```bash
# Run the simulation using the command-line tool
ecosim

# Run with custom settings
ecosim --width 60 --height 30 --days 100 --speed 0.1
```

Alternatively, you can run directly from the source:

```bash
# Navigate to the ecosystem_sim directory
cd ecosystem_sim

# Run the main module
python main.py

# Run with custom settings
python main.py --width 60 --height 30 --days 100 --speed 0.1
```

## Command Line Arguments

- `-w, --width`: Width of the world grid (default: 40)
- `-t, --height`: Height of the world grid (default: 20)
- `-d, --days`: Number of days to simulate (default: 30)
- `-s, --speed`: Simulation speed in seconds per hour (default: 0.2)

## Visualization Legend

- `~`: Water
- `.`: Dry soil
- `:`: Moist soil
- `=`: Wet soil
- `,`: Small plant
- `*`: Medium plant
- `♣`: Large plant

## Future Enhancements

- Add herbivores that eat plants
- Add carnivores that eat herbivores
- Implement a food chain and ecosystem balance
- Add insects for pollination
- Add simulated humans (agents) with critical thinking and adaptability
- Implement a history logging system

## Project Structure

- `main.py`: Main entry point for running the simulation
- `world.py`: Defines the World class that represents the environment grid
- `plant.py`: Defines the Plant class for plant growth and reproduction
- `simulation.py`: Manages the simulation updates and state
- `visualization.py`: Provides ASCII visualization for the simulation 