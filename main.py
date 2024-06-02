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
        "1": "Compute the shortest distance from each site.",
        "2": "Conduct system analysis.",
        # "3": "Compute the nearest neighbor distances for each site.",
    }

    for key, value in options.items():
        print(f"[{key}] {value}")

    choice = input(f"Enter your choice (1-{len(options)}): ")

    if choice == "1":
        bond.run_bond_analysis(script_path)
    elif choice == "2":
        system.run_system_analysis(script_path)
    # elif choice == "3":
    #     environment.run_environment_analysis(script_path)


if __name__ == "__main__":
    main()
