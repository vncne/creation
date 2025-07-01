# 🌱 Ecosystem Simulation

A dynamic, grid-based ecosystem simulation that models plant growth, water cycles, atmospheric conditions, and ecological interactions in a terminal-based environment.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## ✨ Features

- **🌿 Plant Life Cycle**: Realistic plant growth, aging, reproduction, and death
- **🌞 Day/Night Cycle**: Dynamic lighting that affects plant photosynthesis
- **💧 Water System**: Sophisticated water cycle with evaporation, rain, and soil moisture
- **🌍 Grid-Based World**: Customizable world size with different terrain types (soil, water)
- **📊 Real-time Statistics**: Live monitoring of ecosystem health and populations
- **🎮 Interactive Controls**: Adjustable simulation speed and duration
- **🔬 Population Dynamics**: Realistic carrying capacity and resource competition
- **📱 ASCII Visualization**: Beautiful terminal-based graphics

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ecosystem-simulation
   ```

2. **Install dependencies** (if using Poetry):
   ```bash
   poetry install
   poetry shell
   ```

   Or with pip:
   ```bash
   pip install -r requirements.txt  # if available
   ```

3. **Run the simulation**:
   ```bash
   python run_simulation.py
   ```

### Basic Usage

```bash
# Run with default settings (40x20 world, 30 days)
python run_simulation.py

# Custom world size and duration
python run_simulation.py --width 60 --height 30 --days 50

# Faster simulation
python run_simulation.py --speed 0.1

# Get help
python run_simulation.py --help
```

## 🎮 Controls & Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--width` | `-w` | World grid width | 40 |
| `--height` | `-t` | World grid height | 20 |
| `--days` | `-d` | Simulation duration in days | 30 |
| `--speed` | `-s` | Seconds per simulation hour | 0.2 |

### Keyboard Controls
- **Ctrl+C**: Stop simulation gracefully

## 🗺️ Understanding the Display

### World Symbols
- `~` - Water bodies (lakes, rivers)
- `.` - Dry soil (low moisture)
- `:` - Moist soil (medium moisture)  
- `=` - Wet soil (high moisture)
- `,` - Small plants/seedlings
- `*` - Medium plants
- `♣` - Large/mature plants

### Statistics Panel
```
Day: 5 | Hour: 14 | Plants: 45/200
CO2: 98.3 | O2: 101.7 | Atm. Water: 1.2
```

- **Day/Hour**: Current simulation time
- **Plants**: Current population / Maximum allowed
- **CO2/O2**: Atmospheric gas levels
- **Atm. Water**: Water vapor in atmosphere

## 🔬 Simulation Mechanics

### Plant Lifecycle
1. **Germination**: Seeds start as small seedlings (`,`)
2. **Growth**: Plants grow based on sunlight and water availability
3. **Maturity**: Mature plants can reproduce and spread seeds
4. **Aging**: Old plants gradually lose health and die
5. **Decomposition**: Dead plants return nutrients to soil

### Environmental Systems

#### 🌞 Day/Night Cycle
- **Peak sunlight**: 12:00 PM (noon)
- **No light**: 12:00 AM (midnight)
- **Photosynthesis**: Only occurs during daylight hours

#### 💧 Water Cycle
- **Evaporation**: Water evaporates during hot, sunny days
- **Precipitation**: Rain occurs during nights or when atmospheric water is high
- **Soil Moisture**: Affects plant growth and survival

#### 🌱 Population Dynamics
- **Carrying Capacity**: Maximum population based on world size (10% of grid)
- **Resource Competition**: Limited water and space create natural selection pressure
- **Reproduction**: Only healthy, mature plants can reproduce

## 📁 Project Structure

```
ecosystem-simulation/
├── ecosystem_sim/           # Main simulation package
│   ├── __init__.py         # Package initialization
│   ├── simulation.py       # Core simulation logic
│   ├── world.py           # World grid and environment
│   ├── plant.py           # Plant behavior and lifecycle  
│   ├── visualization.py   # ASCII rendering system
│   └── main.py            # CLI interface
├── tests/                  # Test suite
├── run_simulation.py      # Convenience runner script
├── pyproject.toml         # Project configuration
├── BUG_FIXES_REPORT.md   # Recent bug fixes documentation
└── README.md              # This file
```

## 🧪 Examples

### Example 1: Small Garden Simulation
```bash
python run_simulation.py --width 20 --height 15 --days 10 --speed 0.1
```

### Example 2: Large Ecosystem
```bash
python run_simulation.py --width 80 --height 40 --days 100 --speed 0.05
```

### Example 3: Fast Overview
```bash
python run_simulation.py --days 365 --speed 0.01
```

## 🐛 Recent Bug Fixes

The simulation has been recently updated to fix several critical issues:

1. **Daylight Calculation**: Fixed incorrect lighting formula for realistic day/night cycles
2. **Data Integrity**: Added proper encapsulation for world grid modifications  
3. **Population Control**: Implemented carrying capacity to prevent infinite growth

See `BUG_FIXES_REPORT.md` for detailed technical information.

## 🔧 Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Structure
The simulation follows object-oriented design principles:

- **`Simulation`**: Manages overall simulation state and updates
- **`World`**: Handles grid, time, and environmental conditions
- **`Plant`**: Individual plant behavior and lifecycle
- **`AsciiVisualizer`**: Renders simulation state to terminal

### Extending the Simulation

#### Adding New Plant Types
```python
class TreePlant(Plant):
    def __init__(self, position, world):
        super().__init__(position, world)
        self.max_size = 2.0  # Trees grow larger
        self.reproduction_age = 50  # Take longer to mature
```

#### Adding New Terrain Types
```python
# In world.py
cell = {
    'type': 'rock',  # New terrain type
    'light': 0.0,
    'water': 0.0,    # Rocks hold no water
    'temperature': 25.0,
    'resources': 0.1  # Limited nutrients
}
```

## 📊 Performance

- **Memory Usage**: Approximately 1MB per 1000 plants
- **CPU Usage**: Scales linearly with world size and plant population
- **Recommended Limits**:
  - World size: Up to 100x100 for smooth performance
  - Plant population: Up to 1000 plants
  - Simulation speed: 0.01+ seconds per hour

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by Conway's Game of Life and ecological modeling research
- Built with Python's standard library for maximum compatibility
- ASCII art visualization for universal terminal support

## 📞 Support

If you encounter any issues or have questions:
1. Check the `BUG_FIXES_REPORT.md` for known issues
2. Review this README for usage examples
3. Open an issue on the repository

---

*Happy simulating! 🌱*