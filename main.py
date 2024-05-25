"""
Main script for processing CIF files.

This script processes CIF files in a specified directory,
performs preprocessing, bond analysis, and generates output files and plots.

Usage:
    python main.py

Author: Sangjoon Bob Lee

Last update: May 24, 2024
Release date: Mar 10, 2024

"""

import os
from run import bond, system


def main():
    script_path = os.path.dirname(os.path.abspath(__file__))

    print("\nWelcome! Please choose an option to proceed:")
    options = {
        "1": "Compute the shortest distance from each site per file.",
        "2": "Use the result from Option 1 to conduct system analysis",
    }

    for key, value in options.items():
        print(f"[{key}] {value}")

    choice = input("Enter your choice (1-2): ")

    if choice == "1":
        bond.run_bond(script_path)
    elif choice == "2":
        system.run_system_analysis(script_path)


if __name__ == "__main__":
    main()
