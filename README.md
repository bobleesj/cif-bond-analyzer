# CIF Bond Analyzer (CBA)

![Header](https://s9.gifyu.com/images/SViLp.png)

[![Integration tests](https://github.com/bobleesj/cif-bond-analyzer/actions/workflows/python-run-pytest.yml/badge.svg)](https://github.com/bobleesj/cif-bond-analyzer/actions/workflows/python-run-pytest.yml) ![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg) ![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg) ![Python 3.11](https://img.shields.io/badge/python-3.12-blue.svg) 

## Description

CIF Bond Analyzer (CBA) is an interactive, command-line Python application designed for the high-throughput extraction of bonding information from CIF (Crystallographic Information File) file.


### Overview

1. Choose the folder interactively and decided to inculde .cif files in nested folders.
2. Preprocess .cif files and standarlize site labels
3. Move ill-formatted files
4. Choose one of the options
5. Generate a unitcell and a supercell by applying +-1, +-1, +-1 shifts in fractional coordinates.
6. Generate a supercell for each file and determine the shortest distance and pair from each atomic site. The atomic site is selected based on the atom with the greatest number of minimum distances in the surrounding atoms.


## Demo

![CIF Bond Analyzer execution process](https://s12.gifyu.com/images/SViMw.gif)


## How to use

Download all the required libraries. The code has been tested on Python version 3.10, 3.11, 3.12.

```bash
pip install -r requirements.txt
```

This command will start the program and prompt you to select a folder containing .`cif` files for analysis.

```bash
python main.py
```

The following will prompt

```text
Welcome! Please choose an option to proceed:
[1] Conduct site analysis.
[2] Conduct system analysis.
[3] Conduct coordination analysis.
Enter your choice (1-3): 
```

## Options

CBA supports 3 options with details provided below.

###  Option 1. Site Analysis

From a single `.cif` file, a supercell is generated and determines the shortest distance and the connecting site.

#### Output 1.1 text summary

A text file `summary.txt` is generated in the folder to provide an overview of the shortest bonding pairs and missing pairs in the selected folders.

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

#### Output 1.2 histograms

In the `output` folder, histograms per shortest pair distance from each atom will be saved.

![Histograms for label pair](https://s9.gifyu.com/images/SViMv.png)

To modify the histograms, run `python plot-histogram.py`. This script allows you to interactively specify parameters, such as the bin width and x-axis range:

#### Output 1.3 Excel and JSON

For each folder, CBA generates `.xlsx` and `.json` files containing the shortest distance and the connecting site from each reference site.

 It also determines the atomic mixing and occupacny information at the pair level. It extracts the tag from the .cif file if provided.

`site_pairs.json` is produced shown below.

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
                "dist": 2.404,
                "mixing": "full_occupancy",
                "formula": "Er2Co17",
                "tag": "hex",
                "structure": "Th2Ni17"
            },
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
        ],
        "1644636": [
            {
                "dist": 2.49,
                "mixing": "full_occupancy",
                "formula": "ErCo2",
                "tag": "lt",
                "structure": "TbFe2"
            }
        ],
    }
}
```

`element_pairs.json` is generated that it determines the shortest distance for each bond pair in a file.

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
        ],
        "1644636": [
            {
                "dist": 2.49,
                "mixing": "full_occupancy",
                "formula": "ErCo2",
                "tag": "lt",
                "structure": "TbFe2"
            }
        ]
    }
}
```

An Excel file containing the information and each sheet having the bond pair.

[20240623_ErCoIn_nested_element_pairs.xlsx](https://github.com/user-attachments/files/15963693/20240623_ErCoIn_nested_element_pairs.xlsx)

![Excel screenshot](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/d6bed0df-b9ea-4922-967b-4656bb3ab3e0)


```
File	Distance
1814810.cif	2.623
1803318.cif	2.644
1840445.cif	2.691
1818414.cif	2.729
1234747.cif	2.737
1140826.cif	2.743
1229705.cif	2.794
1956508.cif	2.799
1000761.cif	2.81
1233938.cif	2.881
1803512.cif	2.882
1925389.cif	2.922
    
Average	2.771
SD	0.094
```


### Option 2. System Analysis

System Analyiss is applicable for a folder containing either 2 or 3 unique elements. Four types are possible.

```
4 types of folders are processed:
- Type 1. Binary files, 2 unique elements
- Type 2. Binary files, 3 unique elements
- Type 3. Ternary files, 3 unique elements
- Type 4. Ternary and binary combined, 3 unique elements
```

Here is an example below. 
```
Available folders containing 2 or 3 unique elements:
1. 20240623_ErCoIn_nested, 3 elements (In, Er, Co), 152 files
2. 20240612_ternary_only, 3 elements (In, Er, Co), 2 files
3. 20240611_ternary_binary_combined, 3 elements (In, Er, Co), 5 files
4. 20240623_teranry_3_unique_elements, 2 elements (Er, Co), 3 files
5. 20240611_binary_2_unique_elements, 2 elements (Er, Co), 4 files````
```


#### Output 2.1 Binary/ternary figures

By deafult, all of the nested folders containing .cif files are automatically added. 

For Type 1, the following is generated.

For Type 2, 3, 4, the following is generated.

Customizaiton: You move the positino of the legend in the ternary diagram, you may modify the values of `X_SHIFT = 0.0` and `Y_SHIFT = 0.0` in `core/configs/ternary.py`.

Individual hexagons are also produced.

![composite_binary_2](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/b385fe6e-f17e-439d-99e8-694378c097a3)
![composite_ternary_1](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/1cb0b0f8-501e-4c53-86fb-190e304f11a6)


![color_map_Er-In](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/2da0a905-b247-43ac-bebf-4afc4c0b0608)

![color_map_In-In](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/874b083f-1aa3-4bd0-aba3-eb63bf5229e7)

![color_map_overall](https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/1a450ee5-053c-471e-b092-e1731427c2a0)


#### Output 2.2 Color map

Color map for each bond type and the overall is generated for Type 2, 3, 4 above.

#### Output 2.3 Excel

`system_analysis_files.xlsx`

<img width="753" alt="SA_main" src="https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/024b9f0f-5a5f-43ae-8e70-86031db9d26a">


`system_analysis_main.xlsx`

<img width="1025" alt="SA_file" src="https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/420193ec-081a-4df2-b56e-9cddcefa00cb">



### Option 3. Coordination Analysis

#### Ouput 3.1 JSON

It determines the best cooridnation geometry using 4 methods provided in `cifkit`. Save Excel file and JSON on nearest neighbor info. 

The Excel contains ∆ which is defined as the interactomic distance substracted by the sum of atomic radii. Note: For the CN methods, please refer to README.md. Note: ∆ is (interatomic distance - sum of atomic radii).
You may provide your radii values by modifying the radii.xlsx file.


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
                "neighbor": 10
            },
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

A screenshot is provided below. Each sheet contains the file name and the formula associated with the file.

<img width="842" alt="CN_excel" src="https://github.com/bobleesj/cif-bond-analyzer/assets/14892262/6322cacf-5ab0-4855-90e3-56aaddf6ab1f">


## Installation

```bash
git clone https://github.com/bobleesj/cif-bond-analyzer.git
cd cif-bond-analyzer
pip install -r requirements.txt
python main.py
```

If you are interested in using `Conda` with a new environment run the following:

```bash
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

## Questions?

Please feel free to reach out via sl5400@columbia.edu for any questions.


## Changelog

- 20240623 - Implement CN bond fractions, refactor code, nested code, add integration tests
- 20240331 - Added integration test for JSON result verification.
- 20240330 - Added sequential folder processing and customizable histogram generation. See [Pull #16](https://github.com/bobleesj/cif-bond-analyzer/pull/16).
- 20240326 - Implemented automatic preprocessing and relocation of unsupported CIF files.
- 20240311 - Integrated PEP8 linting with `black`. See [Pull #12](https://github.com/bobleesj/cif-bond-analyzer/pull/12).
- 20240310 - Enhanced output options to include both element-based and label-based data for Excel, JSON, and histograms. See [Pull #11](https://github.com/bobleesj/cif-bond-analyzer/pull/11).
- 20240301 - Provided translation options for unit cells with more than 100 atoms, either in all ±1 directions or just +1 in each.
- 20240301 - Displayed atom counts and execution time per file in Terminal; added CSV logging.
- 20240229 - Expanded file support to include all CIF files.
