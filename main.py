"""
Main script for processing CIF files.

This script processes CIF files in a specified directory,
performs preprocessing, bond analysis, and generates output files and plots.

Usage:
    python main.py

Author: Sangjoon Bob Lee

Last update: June 9, 2024
Release date: Mar 10, 2024

"""

import os
from core.run import site, system, coordination


def main():
    script_path = os.path.dirname(os.path.abspath(__file__))

    print("\nWelcome! Please choose an option to proceed:")
    options = {
        "1": "Compute the shortest distance from each site.",
        "2": "Conduct system analysis.",
        "3": "Conduct coordination analysis.",
    }

    for key, value in options.items():
        print(f"[{key}] {value}")

    choice = input(f"Enter your choice (1-{len(options)}): ")

    if choice == "1":
        site.run_site_analysis(script_path)
    elif choice == "2":
        system.run_system_analysis(script_path)
    elif choice == "3":
        coordination.run_coordination(script_path)


if __name__ == "__main__":
    main()
