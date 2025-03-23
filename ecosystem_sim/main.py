"""
Main module for running the ecosystem simulation.
"""
import time
import argparse
from ecosystem_sim.simulation import Simulation
from ecosystem_sim.visualization import AsciiVisualizer

def main():
    """
    Run the ecosystem simulation.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run an ecosystem simulation.')
    parser.add_argument('-w', '--width', type=int, default=40, help='Width of the world grid')
    parser.add_argument('-t', '--height', type=int, default=20, help='Height of the world grid')
    parser.add_argument('-d', '--days', type=int, default=30, help='Number of days to simulate')
    parser.add_argument('-s', '--speed', type=float, default=0.2, help='Simulation speed (seconds per hour)')
    args = parser.parse_args()
    
    # Create the simulation
    print(f"Initializing ecosystem simulation ({args.width}x{args.height})...")
    sim = Simulation(args.width, args.height)
    
    # Create the visualizer
    vis = AsciiVisualizer(sim)
    
    # Run the simulation
    print(f"Starting simulation for {args.days} days...")
    
    try:
        # Run until reaching the target day or user interrupts
        while sim.world.day < args.days:
            vis.clear_screen()
            print(vis.render())
            
            sim.update()
            
            # Sleep to control simulation speed
            time.sleep(args.speed)
        
        # Final state
        vis.clear_screen()
        print(vis.render())
        print("\nSimulation complete!")
        
    except KeyboardInterrupt:
        print("\nSimulation terminated by user.")

if __name__ == "__main__":
    main()
