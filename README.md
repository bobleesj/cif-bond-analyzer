# CIF Bond Analyzer (CBA)

![Header](https://s9.gifyu.com/images/SViLp.png)

## Description

CIF Bond Analyzer (CBA) is an interactive, command-line Python application designed for the high-throughput extraction of minimum bond length and atomic mixing information from a CIF (Crystallographic Information File) file. CBA constructs a supercell and determines the minimum bond length from each atomic site. CBA repeats the extraction process for each file in the selected folder. The outputs are saved in both JSON and Excel formats. Additionally, CBA generates histograms for a graphical overview of bond lengths and a text file that enumerates bond pair counts and unobserved bonding pairs.

## What CIF Bond Anaylzer does

1. Preprocess Crystallographic Information Files (CIF) from selected folders.
2. Generate a supercell for each file and determine the shortest distance and pair from each atomic site.
3. Generate histograms and save the data in text and Excel file formats.

## Usage

This command will start the program and prompt you to select a folder containing .`cif` files for analysis.

```python
python main.py
```

When you run `python main.py`, it identifies folders containing `.cif` files.

```bash
Folders with .cif files:
1. 20240308_output_test, 12 files
2. 20240307_histogram_test, 41 files

Would you like to process each folder above sequentially?
(Default: Y) [Y/n]: y
```

To modify the histogram width and customize histogram generation, use `plot-histogram.py`. This script allows you to interactively specify parameters, such as the bin width and x-axis range:

```python
python plot-histogram.py
```



## Demo

![CIF Bond Analyzer execution process](https://s12.gifyu.com/images/SViMw.gif)

### Output 1. Text file

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

### Output 2. Histograms

In the `output` folder, histograms per shortest pair distance from each atom will be saved.

![Histograms for label pair](https://s9.gifyu.com/images/SViMv.png)

### Output 3. Excel and JSON

```json
{
    "Ni-Ni": {
        "1830597": [
            {
                "mixing": "4",
                "dist": "2.477"
            }
        ]
    },
    "Ni-Ga": {
        "1830597": [
            {
                "mixing": "4",
                "dist": "2.53"
            },
            {
                "mixing": "3",
                "dist": "2.424"
            }
        ]
    }
}
```

Atomic mixing info mapping:

```python
categories_mapping = {
      "1": "Deficiency with atomic mixing",
      "2": "Full occupancy with atomic mixing",
      "3": "Deficiency without atomic mixing",
      "4": "Full occupancy",
  }
```

## Installation

Simply copy and paste the following block.

```bash
git clone https://github.com/bobleesj/cif-bond-analyzer.git
cd cif-bond-analyzer
pip install pandas click gemmi matplotlib pytest sympy openpyxl
python main.py
```

The above method had no issue so far. But If you are interested in using `Conda` with a new environment run the following:

```bash
git clone https://github.com/bobleesj/cif-bond-analyzer.git
cd cif-bond-analyzer
conda create -n cif python=3.12
conda activate cif
pip install -r requirements.txt
python main.py
```

## Tutorial

> If you are new to Conda (Python package manager), I have written a tutorial for you here [Intro to Python package manager for beginners (Ft. Conda with Cheatsheet](https://bobleesj.github.io/tutorial/2024/02/26/intro-to-python-package-manager.html).


## Contributors

- Anton Oliynyk
- Emil Jaffal
- Sangjoon Bob Lee

## Questions?

Please feel free to reach out via sl5400@columbia.edu for any questions 

## How to contribute or report a bug

Please feel free to report an issue or contribute by making a new issue [here](https://github.com/bobleesj/cif-bond-analyzer/issues)

## Changelog

- 20240331 - Added integration test for JSON result verification.
- 20240330 - Added sequential folder processing and customizable histogram generation. See [Pull #16](https://github.com/bobleesj/cif-bond-analyzer/pull/16).
- 20240326 - Implemented automatic preprocessing and relocation of unsupported CIF files.
- 20240311 - Integrated PEP8 linting with `black`. See [Pull #12](https://github.com/bobleesj/cif-bond-analyzer/pull/12).
- 20240310 - Enhanced output options to include both element-based and label-based data for Excel, JSON, and histograms. See [Pull #11](https://github.com/bobleesj/cif-bond-analyzer/pull/11).
- 20240301 - Provided translation options for unit cells with more than 100 atoms, either in all ±1 directions or just +1 in each.
- 20240301 - Displayed atom counts and execution time per file in Terminal; added CSV logging.
- 20240229 - Expanded file support to include all CIF files.
