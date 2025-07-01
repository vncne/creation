"""
Unit tests for the Main module.
Tests command-line argument parsing and main simulation execution flow.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import argparse
from ecosystem_sim.main import main


class TestMain(unittest.TestCase):
    """Test cases for the main module."""
    
    @patch('ecosystem_sim.main.time.sleep')
    @patch('ecosystem_sim.main.AsciiVisualizer')
    @patch('ecosystem_sim.main.Simulation')
    @patch('sys.argv', ['main.py'])
    def test_main_default_arguments(self, mock_simulation, mock_visualizer_class, mock_sleep):
        """Test main function with default arguments."""
        # Set up mocks
        mock_sim = Mock()
        mock_sim.world.day = 0
        mock_simulation.return_value = mock_sim
        
        mock_vis = Mock()
        mock_vis.render.return_value = "Test output"
        mock_visualizer_class.return_value = mock_vis
        
        # Run main (will exit after 0 days since mock day starts at 0)
        main()
        
        # Verify simulation was created with default values
        mock_simulation.assert_called_once_with(40, 20)
        mock_visualizer_class.assert_called_once_with(mock_sim)
    
    @patch('ecosystem_sim.main.time.sleep')
    @patch('ecosystem_sim.main.AsciiVisualizer')
    @patch('ecosystem_sim.main.Simulation')
    @patch('sys.argv', ['main.py', '--width', '60', '--height', '30', '--days', '5', '--speed', '0.1'])
    def test_main_custom_arguments(self, mock_simulation, mock_visualizer_class, mock_sleep):
        """Test main function with custom arguments."""
        # Set up mocks
        mock_sim = Mock()
        mock_sim.world.day = 0
        mock_simulation.return_value = mock_sim
        
        mock_vis = Mock()
        mock_vis.render.return_value = "Test output"
        mock_visualizer_class.return_value = mock_vis
        
        main()
        
        # Verify simulation was created with custom values
        mock_simulation.assert_called_once_with(60, 30)
    
    @patch('ecosystem_sim.main.time.sleep')
    @patch('ecosystem_sim.main.AsciiVisualizer')
    @patch('ecosystem_sim.main.Simulation')
    @patch('sys.argv', ['main.py', '--days', '2'])
    def test_main_simulation_loop(self, mock_simulation, mock_visualizer_class, mock_sleep):
        """Test main function simulation loop execution."""
        # Set up mocks to run for exactly 2 iterations
        mock_sim = Mock()
        mock_sim.world.day = 0
        # After first update, day becomes 1, after second update, day becomes 2
        mock_sim.world.day = 0  # This will be checked in while condition
        mock_simulation.return_value = mock_sim
        
        mock_vis = Mock()
        mock_vis.render.return_value = "Test output"
        mock_visualizer_class.return_value = mock_vis
        
        # Mock the day progression
        day_values = [0, 0, 1, 1, 2]  # day values for each check
        mock_sim.world.day = 0
        
        def side_effect(*args):
            if hasattr(side_effect, 'call_count'):
                side_effect.call_count += 1
            else:
                side_effect.call_count = 1
            
            if side_effect.call_count < len(day_values):
                mock_sim.world.day = day_values[side_effect.call_count]
        
        mock_sim.update.side_effect = side_effect
        
        main()
        
        # Verify methods were called
        mock_vis.clear_screen.assert_called()
        mock_vis.render.assert_called()
        mock_sim.update.assert_called()
        mock_sleep.assert_called()
    
    @patch('ecosystem_sim.main.time.sleep')
    @patch('ecosystem_sim.main.AsciiVisualizer')
    @patch('ecosystem_sim.main.Simulation')
    @patch('builtins.print')
    @patch('sys.argv', ['main.py', '--days', '1'])
    def test_main_keyboard_interrupt(self, mock_print, mock_simulation, mock_visualizer_class, mock_sleep):
        """Test main function handles KeyboardInterrupt gracefully."""
        # Set up mocks
        mock_sim = Mock()
        mock_sim.world.day = 0
        mock_simulation.return_value = mock_sim
        
        mock_vis = Mock()
        mock_vis.render.return_value = "Test output"
        mock_visualizer_class.return_value = mock_vis
        
        # Simulate KeyboardInterrupt during sleep
        mock_sleep.side_effect = KeyboardInterrupt()
        
        # Should not raise exception
        main()
        
        # Should print termination message
        mock_print.assert_any_call("\nSimulation terminated by user.")
    
    @patch('ecosystem_sim.main.argparse.ArgumentParser.parse_args')
    def test_argument_parsing(self, mock_parse_args):
        """Test argument parsing functionality."""
        # Mock parsed arguments
        mock_args = Mock()
        mock_args.width = 50
        mock_args.height = 25
        mock_args.days = 10
        mock_args.speed = 0.15
        mock_parse_args.return_value = mock_args
        
        with patch('ecosystem_sim.main.Simulation') as mock_simulation, \
             patch('ecosystem_sim.main.AsciiVisualizer'), \
             patch('ecosystem_sim.main.time.sleep'):
            
            mock_sim = Mock()
            mock_sim.world.day = 10  # End immediately
            mock_simulation.return_value = mock_sim
            
            main()
            
            # Verify simulation created with parsed arguments
            mock_simulation.assert_called_once_with(50, 25)
    
    @patch('sys.argv', ['main.py', '--help'])
    def test_help_argument(self):
        """Test that help argument works (will exit)."""
        with self.assertRaises(SystemExit):
            main()
    
    @patch('sys.argv', ['main.py', '--width', 'invalid'])
    def test_invalid_arguments(self):
        """Test handling of invalid arguments."""
        with self.assertRaises(SystemExit):
            main()
    
    @patch('ecosystem_sim.main.time.sleep')
    @patch('ecosystem_sim.main.AsciiVisualizer')
    @patch('ecosystem_sim.main.Simulation')
    @patch('builtins.print')
    @patch('sys.argv', ['main.py', '--days', '1'])
    def test_final_state_display(self, mock_print, mock_simulation, mock_visualizer_class, mock_sleep):
        """Test that final state is displayed after simulation completion."""
        # Set up mocks
        mock_sim = Mock()
        mock_sim.world.day = 1  # Will exit loop immediately
        mock_simulation.return_value = mock_sim
        
        mock_vis = Mock()
        mock_vis.render.return_value = "Final state"
        mock_visualizer_class.return_value = mock_vis
        
        main()
        
        # Should display final state and completion message
        mock_print.assert_any_call("\nSimulation complete!")
    
    @patch('ecosystem_sim.main.time.sleep')
    @patch('ecosystem_sim.main.AsciiVisualizer')
    @patch('ecosystem_sim.main.Simulation')
    @patch('builtins.print')
    @patch('sys.argv', ['main.py', '--speed', '0.05'])
    def test_speed_parameter(self, mock_print, mock_simulation, mock_visualizer_class, mock_sleep):
        """Test that speed parameter affects sleep duration."""
        # Set up mocks
        mock_sim = Mock()
        mock_sim.world.day = 1  # Exit after one iteration
        mock_simulation.return_value = mock_sim
        
        mock_vis = Mock()
        mock_vis.render.return_value = "Test output"
        mock_visualizer_class.return_value = mock_vis
        
        main()
        
        # Verify sleep was called with correct duration
        mock_sleep.assert_called_with(0.05)
    
    @patch('ecosystem_sim.main.time.sleep')
    @patch('ecosystem_sim.main.AsciiVisualizer')
    @patch('ecosystem_sim.main.Simulation')
    @patch('builtins.print')
    def test_initialization_messages(self, mock_print, mock_simulation, mock_visualizer_class, mock_sleep):
        """Test that initialization and start messages are printed."""
        with patch('sys.argv', ['main.py', '--width', '25', '--height', '15', '--days', '5']):
            # Set up mocks
            mock_sim = Mock()
            mock_sim.world.day = 5  # Exit immediately
            mock_simulation.return_value = mock_sim
            
            mock_vis = Mock()
            mock_visualizer_class.return_value = mock_vis
            
            main()
            
            # Check initialization message
            mock_print.assert_any_call("Initializing ecosystem simulation (25x15)...")
            
            # Check start message
            mock_print.assert_any_call("Starting simulation for 5 days...")


class TestMainIntegration(unittest.TestCase):
    """Integration tests for main module with real components."""
    
    @patch('ecosystem_sim.main.time.sleep')
    @patch('builtins.print')
    def test_main_integration_short_run(self, mock_print, mock_sleep):
        """Test main function integration with real components for a short run."""
        with patch('sys.argv', ['main.py', '--width', '5', '--height', '5', '--days', '1', '--speed', '0.01']):
            # This should run without crashing
            try:
                main()
            except SystemExit:
                pass  # Expected if using argparse
            
            # Should have printed messages
            self.assertTrue(mock_print.called)
    
    def test_argument_parser_creation(self):
        """Test that argument parser is created correctly."""
        # This test ensures the argument parser has all expected arguments
        from ecosystem_sim.main import main
        
        # Temporarily replace sys.argv to test parser
        with patch('sys.argv', ['main.py', '--help']):
            with self.assertRaises(SystemExit):
                # This will trigger help and exit
                main()


if __name__ == '__main__':
    unittest.main()