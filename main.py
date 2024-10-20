"""
Main script for conducting 3 analysis options.

Usage:
    python main.py

Author: Sangjoon Bob Lee
"""

import os
from core.run import coordination_analysis, site_analysis, system_analysis


def main():
    script_path = os.path.dirname(os.path.abspath(__file__))

    print("\nWelcome! Please choose an option to proceed:")
    options = {
        "1": "Conduct site analysis.",
        "2": "Conduct system analysis.",
        "3": "Conduct coordination analysis.",
    }

    for key, value in options.items():
        print(f"[{key}] {value}")

    choice = input(f"Enter your choice (1-{len(options)}): ")

    if choice == "1":
        site_analysis.run_site_analysis(script_path)
    elif choice == "2":
        system_analysis.run_system_analysis(script_path)
    elif choice == "3":
        coordination_analysis.run_coordination(script_path)


if __name__ == "__main__":
    main()
