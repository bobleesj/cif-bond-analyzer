import textwrap
import click


def prompt_site_analysis_intro() -> None:
    intro_prompt = textwrap.dedent(
        """
        ==========================SITE ANALYSIS=============================
        Process for Site Analysis:

        [1] Preprocess and standardize atomic labels in each .cif file
        [2] Form supercell by shifting unitcell by +-1, +-1, +-1
        [3] Determine shortest unique atomic pairs and atomic mixing
        [4] Indicate frequency and distances of bonding pairs
        [5] Identify missing atomic pairs not observed across all CIF files
        [6] Generate histograms for each unique atomic pair

        Let's get started!
        =====================================================================
        """
    )
    print(intro_prompt)


def prompt_system_analysis_intro() -> None:
    intro_prompt = textwrap.dedent(
        """
        ============================SYSTEN ANALYSIS==========================
        Process for System Analysis:

        4 types of folders are processed:
        - Type 1. Binary files, 2 unique elements
        - Type 2. Binary files, 3 unique elements
        - Type 3. Ternary files, 3 unique elements
        - Type 4. Ternary and binary combined, 3 unique elements

        Note: Nested folders containing .cif files are automatically added.
        Note: Please refer to README.md for visualizations and Excel files.
        ======================================================================
        """
    )
    click.echo(intro_prompt)


def prompt_coordination_analysis_intro() -> None:
    intro_prompt = textwrap.dedent(
        """
        =========================COORDINAITON ANALYSIS=======================
        Process for Coordination Analaysis:

        [1] Preprocess and standardize atomic labels in each .cif file
        [2] Form supercell by shifting unitcell by +-1, +-1, +-1
        [3] Determine the best coordination geometry from 4 methods
        [4] Save Excel file and JSON on nearest neighbor info
        
        Note: For the CN methods, please refer to README.md
        Note: ∆ is (interatomic distance - sum of atomic radii).
        You may provide your radii values by modifying the radii.xlsx file.
        ======================================================================
        """
    )
    click.echo(intro_prompt)


def prompt_plot_histograms_intro() -> None:
    intro_prompt = textwrap.dedent(
        """
        ============================PLOT HISTOGRAMS===========================
        Process for re-plotting histograms:

        Note: Folder must contain .json produced from Site Analysis.
        Note: Customize bin size, min and max x-value in all histograms.
        ======================================================================
        """
    )
    click.echo(intro_prompt)
