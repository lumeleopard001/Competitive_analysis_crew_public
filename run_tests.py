#!/usr/bin/env python3
"""
Test runner script for Competitive Analysis Crew.

This script provides a convenient way to run all tests with various options.
"""

import subprocess
import sys
from pathlib import Path


def run_tests(coverage=False, verbose=False, specific_test=None):
    """
    Run the test suite with optional coverage and verbosity.
    
    Args:
        coverage (bool): Whether to run with coverage reporting
        verbose (bool): Whether to run with verbose output
        specific_test (str): Specific test file or test to run
    """
    cmd = ["python", "-m", "pytest"]
    
    if specific_test:
        cmd.append(specific_test)
    else:
        cmd.append("tests/")
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend([
            "--cov=src/Competitive_analysis_crew/tools",
            "--cov-report=term-missing",
            "--cov-report=html"
        ])
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode


def main():
    """Main entry point for the test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run tests for Competitive Analysis Crew")
    parser.add_argument("--coverage", "-c", action="store_true", 
                       help="Run tests with coverage reporting")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Run tests with verbose output")
    parser.add_argument("--test", "-t", type=str,
                       help="Run specific test file or test")
    
    args = parser.parse_args()
    
    exit_code = run_tests(
        coverage=args.coverage,
        verbose=args.verbose,
        specific_test=args.test
    )
    
    if exit_code == 0:
        print("\n✅ All tests passed!")
        if args.coverage:
            print("📊 Coverage report generated in htmlcov/")
    else:
        print("\n❌ Some tests failed!")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()