"""
Test suite runner for the ecosystem simulation project.
Runs all unit tests and provides comprehensive reporting.
"""
import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import all test modules
from tests.test_world import TestWorld
from tests.test_plant import TestPlant
from tests.test_simulation import TestSimulation
from tests.test_visualization import TestAsciiVisualizer
from tests.test_main import TestMain, TestMainIntegration


def create_test_suite():
    """
    Create a comprehensive test suite with all tests.
    
    Returns:
        unittest.TestSuite: Complete test suite
    """
    suite = unittest.TestSuite()
    
    # Add World tests
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestWorld))
    
    # Add Plant tests
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPlant))
    
    # Add Simulation tests
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSimulation))
    
    # Add Visualization tests
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAsciiVisualizer))
    
    # Add Main tests
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMain))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMainIntegration))
    
    return suite


def run_tests_with_coverage():
    """
    Run tests with coverage reporting if coverage.py is available.
    
    Returns:
        unittest.TestResult: Test results
    """
    try:
        import coverage  # type: ignore
        
        # Start coverage measurement
        cov = coverage.Coverage()
        cov.start()
        
        # Run tests
        suite = create_test_suite()
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Stop coverage and report
        cov.stop()
        cov.save()
        
        print("\n" + "="*50)
        print("COVERAGE REPORT")
        print("="*50)
        cov.report(show_missing=True)
        
        # Generate HTML coverage report
        try:
            cov.html_report(directory='htmlcov')
            print(f"\nHTML coverage report generated in 'htmlcov/' directory")
        except Exception as e:
            print(f"Could not generate HTML report: {e}")
        
        return result
        
    except ImportError:
        print("Coverage.py not available. Running tests without coverage.")
        suite = create_test_suite()
        runner = unittest.TextTestRunner(verbosity=2)
        return runner.run(suite)


def run_specific_module_tests(module_name):
    """
    Run tests for a specific module.
    
    Args:
        module_name (str): Name of the module to test ('world', 'plant', etc.)
    
    Returns:
        unittest.TestResult: Test results
    """
    module_map = {
        'world': TestWorld,
        'plant': TestPlant,
        'simulation': TestSimulation,
        'visualization': TestAsciiVisualizer,
        'main': TestMain
    }
    
    if module_name not in module_map:
        print(f"Unknown module: {module_name}")
        print(f"Available modules: {', '.join(module_map.keys())}")
        return None
    
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(module_map[module_name]))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


def print_test_summary(result):
    """
    Print a comprehensive test summary.
    
    Args:
        result (unittest.TestResult): Test results to summarize
    """
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    
    success_rate = ((total_tests - failures - errors) / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total tests run: {total_tests}")
    print(f"Successful: {total_tests - failures - errors}")
    print(f"Failures: {failures}")
    print(f"Errors: {errors}")
    print(f"Skipped: {skipped}")
    print(f"Success rate: {success_rate:.1f}%")
    
    if failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    print("="*60)
    
    return success_rate == 100.0


def main():
    """
    Main test runner function.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Run ecosystem simulation tests')
    parser.add_argument('--module', '-m', 
                       help='Run tests for specific module (world, plant, simulation, visualization, main)')
    parser.add_argument('--coverage', '-c', action='store_true',
                       help='Run tests with coverage reporting')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    print("Ecosystem Simulation Test Suite")
    print("="*40)
    
    if args.module:
        print(f"Running tests for module: {args.module}")
        result = run_specific_module_tests(args.module)
    elif args.coverage:
        print("Running all tests with coverage...")
        result = run_tests_with_coverage()
    else:
        print("Running all tests...")
        suite = create_test_suite()
        verbosity = 2 if args.verbose else 1
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
    
    if result:
        all_passed = print_test_summary(result)
        sys.exit(0 if all_passed else 1)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()