import textwrap


def prompt_site_analysis_intro():
    intro_prompt = textwrap.dedent(
        """
    ===
    Process for site analysis:
                                   
    [1] Preprocess and standardize atomic labels in each .cif file
    [2] Forms supercell by shifting unitcell by +-1, +-1, +-1
    [3] Determines shortest unique atomic pairs and atomic mixing
    [4] Indicates frequency and distances of bonding pairs.
    [5] Identifies missing atomic pairs not observed across all CIF files.
    [6] Generates histograms for each unique atomic pair.
                                    
    Let's get started!
    ===
    """
    )
    print(intro_prompt)
