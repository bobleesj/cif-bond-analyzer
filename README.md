# CIF Bond Analyzer (CBA)

![Header](https://s9.gifyu.com/images/SViLp.png)

[![Integration tests](https://github.com/bobleesj/cif-bond-analyzer/actions/workflows/python-run-pytest.yml/badge.svg)](https://github.com/bobleesj/cif-bond-analyzer/actions/workflows/python-run-pytest.yml)
![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
![Python 3.11](https://img.shields.io/badge/python-3.12-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/bobleesj/cifkit/blob/main/LICENSE)

The CIF Bond Analyzer (CBA) is an interactive, command-line-based application
designed for high-throughput extraction of bonding information from CIF
(Crystallographic Information File) files. CBA offers Site Analysis, System
Analysis for binary/ternary systems, and Coordination Analysis. The outputs are
saved in `.json`, `.xlsx`, and `.png`formats. 

> The current README.md serves as a tutorial and documentation - last update July 9, 2024

## Demo

The code is designed for interactive use without the need to write any code.

![CBA-demo-gif](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/fad16f21-93d8-4954-8efe-c04fbc68a9b7)


## Scope

Any `.cif` files.

## Value

`CBA` simplifies crystal structure analysis by automating the extraction of
minimum bond lengths, which are crucial for understanding geometric
configurations and identifying irregularities. Histograms and figures assist in
identifying distinct bond lengths and structural patterns.


## Getting started

Copy each line into your command-line applications:

```bash
$ git clone https://github.com/bobleesj/cif-bond-analyzer.git
$ cd cif-bond-analyzer
$ pip install -r requirements.txt
$ python main.py
```

Once the code is executed using `python main.py`, the following prompt will
appear, asking you to choose one of the three analysis options:

```text
Welcome! Please choose an option to proceed:
[1] Conduct site analysis.
[2] Conduct system analysis.
[3] Conduct coordination analysis.
Enter your choice (1-3): 1
```

For any option, CBA will ask you to choose folders containing `.cif` files:

```text

Folders with .cif files:
1. 20240623_ErCoIn_nested, 16 files, 136 nested files
2. 20240612_ternary_only, 2 files
3. 20240611_ternary_binary_combined, 5 files
4. 20240623_teranry_3_unique_elements, 3 files
5. 20240611_binary_2_unique_elements, 4 files

Would you like to process each folder above sequentially?
(Default: Y) [Y/n]:
```

You may then choose to process folders either sequentially or select specific
folders by entering numbers associated with the folders prompted. For each
folder, CBA generates site pair data saved in `site_pairs.json` or
`site_pairs.xlsx`.

## Preprocess

The following discusses formatting, supercell generation, and atomic mixing
information.

### 1. Format files

CBA uses the `CifEnsemble` object from `cifkit` (https://github.com/bobleesj/cifkit) to conduct preprocessing
automatically.

- CBA standardizes the site labels in `atom_site_label`. Some site labels may
  contain a comma or a symbol such as `M` due to atomic mixing. CBA reformats
  each `atom_site_label` so it can be parsed into an element type that matches
  `atom_site_type_symbol`.

- CBA removes the content of `publ_author_address`. This section often has an
  incorrect format that otherwise requires manual modifications.

- CBA relocates any ill-formatted files, such as those with duplicate labels in
  `atom_site_label`, missing fractional coordinates, or files that require
  supercell generation.

### 2. Supercell generation

For each `.cif` file, a unit cell is generated by applying the symmetry
operations. A supercell is generated by applying ±1 shifts from the unit cell.

### 3. Atomic mixing info

Each bonding pair is defined with one of four atomic mixing categories:

- **Full occupancy** is assigned when a single atomic site occupies the
  fractional coordinate with an occupancy value of 1.
- **Full occupancy with mixing** is assigned when multiple atomic sites
  collectively occupy the fractional coordinate to a sum of 1.
- **Deficiency without mixing** is assigned when a single atomic site occupying
  the fractional coordinate with a sum less than 1.
- **Deficiency with atomic mixing** is assigned when multiple atomic sites
  occupy the fractional coordinate with a sum less than 1.

## Analysis Options

CBA provides three options for analysis.

### Option 1. Site Analysis

- **Purpose:** Site Analysis determines the shortest distance and its nearest
  neighbor for each label in `atom_site_label`.

- **Process:** For each atom in the unit cell, Euclidean distances are
  calculated from the atom to all atoms in the supercell. The position of the
  atom in the unit cell for each site label is determined based on the atom with
  the greatest number of shortest distances to its neighbors.

- **Example:** If a `.cif` file under `atom_site_label` contains four site
  labels: `Er1`, `Er2`, `Er3`, and `Er4`. The bonding pair from the site label
  `Er4` and its nearest neighbor `Er2` is unique and recorded. The bonding pair
  from `Er3` to `Er2` is also considered unique. However, the pairs `Er4-Er2`
  and `Er2-Er4` are considered identical. Out of the two pairs, the pair with
  the shorter distance is recorded below.

#### Output 1.1 Excel and JSON

Data for each folder is saved in `site_pairs.json` or `site_pairs.xlsx`. Below
is an example of the JSON structure for bond pairs:

```json
{
  "Co-Co": {
    "250361": [
      {
        "dist": 2.529,
        "mixing": "full_occupancy",
        "formula": "ErCo2",
        "tag": "rt",
        "structure": "MgCu2"
      }
    ],
    "1955204": [
      {
        "dist": 2.46,
        "mixing": "full_occupancy",
        "formula": "Er2Co17",
        "tag": "hex",
        "structure": "Th2Ni17"
      },
      {
        "dist": 2.274,
        "mixing": "full_occupancy",
        "formula": "Er2Co17",
        "tag": "hex",
        "structure": "Th2Ni17"
      }
    ]
  }
}
```

The minimum bond pair for each file is saved in `element_pairs.json` and
`element_pairs.xlsx`.

```json
{
  "Co-Co": {
    "250361": [
      {
        "dist": 2.529,
        "mixing": "full_occupancy",
        "formula": "ErCo2",
        "tag": "rt",
        "structure": "MgCu2"
      }
    ],
    "1955204": [
      {
        "dist": 2.274,
        "mixing": "full_occupancy",
        "formula": "Er2Co17",
        "tag": "hex",
        "structure": "Th2Ni17"
      }
    ]
  }
}
```

Here is a screenshot of `element_pairs.xlsx`.

![Excel screenshot](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/d6bed0df-b9ea-4922-967b-4656bb3ab3e0)

#### Output 1.2 text summary

A summary text file, `summary_element.txt`, lists the shortest bonding pairs and
identifies missing pairs across selected folders:

```txt
Summary:
Pair: In-In, Count: 4, Distances: 2.736, 2.782, 2.785, 2.793
Pair: Pd-Ge, Count: 4, Distances: 2.449, 2.455, 2.489, 2.672
Pair: Pd-Sb, Count: 4, Distances: 2.505, 2.700, 2.737, 2.793
Pair: Si-Si, Count: 4, Distances: 1.975, 2.289, 2.325, 2.533
Pair: Rh-Ge, Count: 2, Distances: 2.484, 2.495
Pair: Ru-Si, Count: 2, Distances: 2.394, 2.519
Pair: Sb-Sb, Count: 2, Distances: 2.573, 2.793
Pair: Co-Ga, Count: 1, Distances: 2.485
Pair: Co-Sb, Count: 1, Distances: 2.594
Pair: Co-Sn, Count: 1, Distances: 2.737

Missing pairs:
Co-In
Co-Ir
Co-Ni
Co-Pd
Co-Pt
Co-Rh
Co-Si
Fe-Co
```

#### Output 1.3 histograms

`histogram_element_pair.png` and `histogram_site_pair.png` are used visualize
data, with colors indicating atomic mixing types.

- To modify the x-axis, run `python plot-histogram.py`. This script allows you
  to interactively specify parameters such as the bin width and x-axis range:

![Histograms for label pair](https://s9.gifyu.com/images/SViMv.png)

### Option 2. System Analysis

- **Purpose:** System Analysis provides an overview of bond fractions acquired
  from Option 1: Site Analysis, or bond fractions in coordination number
  geometries.

- **Scope:** System Analysis is applicable for folders containing either 2 or 3
  unique elements.

4 types of folders are applicable for System Analysis.

- Type 1. Binary files, 2 unique elements
- Type 2. Binary files, 3 unique elements
- Type 3. Ternary files, 3 unique elements
- Type 4. Ternary and binary combined, 3 unique elements

Here is an example of CBA detecting folders containing 2 or 3 unique elements.

`````
Available folders containing 2 or 3 unique elements:
1. 20240623_ErCoIn_nested, 3 elements (In, Er, Co), 152 files
2. 20240612_ternary_only, 3 elements (In, Er, Co), 2 files
3. 20240611_ternary_binary_combined, 3 elements (In, Er, Co), 5 files
4. 20240623_teranry_3_unique_elements, 2 elements (Er, Co), 3 files
5. 20240611_binary_2_unique_elements, 2 elements (Er, Co), 4 files````
`````

#### Output 2.1 Binary/ternary figures

For Types 2, 3, and 4:

![ternary](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/7496f433-c218-49ac-8372-cb75a369e409)

To customize the legend position in the ternary diagram, you may modify the
values of `X_SHIFT = 0.0` and `Y_SHIFT = 0.0` in `core/configs/ternary.py`.

For Type 1:

![binary_single](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/21f25fb3-79ea-4cd1-931d-ad5b3ea55189)

All of the individual hexagon figures also saved in order.

![composite_binary_1](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/3c405d7c-2a42-4114-ba45-d3df0f721b48)

#### Output 2.2 Color map

For Types 2, 3, and 4, color maps for each bond type and overall are generated.

![color_map_overall](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/f5ca3dd2-c6cb-40b8-aff9-af2be90c700f)

![color_map_In-In](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/8f6bd208-9e4d-4dfe-a6a1-04b70af1aacc)

#### Output 2.3 Excel

Bond count per each `cif` file is recorded in `system_analysis_files.xlsx`.

<img width="753" alt="SA_main" src="https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/024b9f0f-5a5f-43ae-8e70-86031db9d26a">

Average bond lenghts, count, and statistical values are recorded in
`system_analysis_main.xlsx`.

<img width="1025" alt="SA_file" src="https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/420193ec-081a-4df2-b56e-9cddcefa00cb">

### Option 3. Coordination Analysis

- **Purpose:** This option determines the best coordination geometry using four
  methods provided in `cifkit`. Excel files and JSON are saved with nearest
  neighbor information.

- **Customization:** The Excel contains `Δ`, which is defined as the interatomic
  distance subtracted by the sum of atomic radii. You may provide your radii
  values by modifying the `radii.xlsx` file.

#### Ouput 3.1 JSON

For each site, the nearest neighbors within the coordination number geometry are
recorded in `CN_connections.json`.

```python
{
    "250361": {
        "Co": [
            {
                "connected_label": "Co",
                "distance": 2.529,
                "delta": 1.16,
                "mixing": "full_occupancy",
                "neighbor": 1
            },
            {
                "connected_label": "Co",
                "distance": 2.529,
                "delta": 1.16,
                "mixing": "full_occupancy",
                "neighbor": 2
            },
            ...
            {
                "connected_label": "Er",
                "distance": 2.966,
                "delta": -0.603,
                "mixing": "full_occupancy",
                "neighbor": 11
            },
            {
                "connected_label": "Er",
                "distance": 2.966,
                "delta": -0.603,
                "mixing": "full_occupancy",
                "neighbor": 12
            }
        ]
    }
}
```

#### Output 3.2 Excel

For each `.cif` file, the nearest neighbor information is wrriten in each sheet
within `CN_connections.xlsx`.

<img width="842" alt="CN_excel" src="https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/6322cacf-5ab0-4855-90e3-56aaddf6ab1f">

## Installation

```text
git clone https://github.com/bobleesj/cif-bond-analyzer.git
cd cif-bond-analyzer
pip install -r requirements.txt
python main.py
```

If you are interested in using `Conda` with a new environment run the following:

```text
git clone https://github.com/bobleesj/cif-bond-analyzer.git
cd cif-bond-analyzer
conda create -n cif python=3.12
conda activate cif
pip install -r requirements.txt
python main.py
```

## Contributors

- Anton Oliynyk
- Emil Jaffal
- Sangjoon Bob Lee

## How to ask for help

`CBA` is also designed for experimental materials scientists and chemists.

- If you have any issues or questions, please feel free to reach out or
  [leave an issue](https://github.com/bobleesj/cif-bond-analyzer/issues).

## How to contribute

Here is how you can contribute to the `CBA` project if you found it helpful:

- Star the repository on GitHub and recommend it to your colleagues who might
  find `CBA` helpful as well.
  [![Star GitHub repository](https://img.shields.io/github/stars/bobleesj/cif-bond-analyzer.svg?style=social)](https://github.com/bobleesj/cif-bond-analyzer/stargazers)
- Fork the repository and consider contributing changes via a pull request.
  [![Fork GitHub repository](https://img.shields.io/github/forks/bobleesj/cif-bond-analyzer?style=social)](https://github.com/bobleesj/cif-bond-analyzer/network/members)
- If you have any suggestions or need further clarification on how to use
  `CBA`, please feel free to reach out to Sangjoon Bob Lee
  ([@bobleesj](https://github.com/bobleesj)).

## Changelog

- 20240623 - Implement CN bond fractions, add GitHub CI. See
  [Pull #22](https://github.com/bobleesj/cif-bond-analyzer/pull/22).
- 20240330 - Add sequential folder processing and customizable histogram
  generation. See
  [Pull #16](https://github.com/bobleesj/cif-bond-analyzer/pull/16).
- 20240311 - Integrate PEP8 linting with `black`. See
  [Pull #12](https://github.com/bobleesj/cif-bond-analyzer/pull/12).
- 20240310 - Enhance output options to include both element-based and
  label-based data for Excel, JSON, and histograms. See
  [Pull #11](https://github.com/bobleesj/cif-bond-analyzer/pull/11).
- 20240301 - Display atom counts and execution time per file in Terminal; adds
  CSV logging.
- 20240229 - Expand file support to include all CIF files.
