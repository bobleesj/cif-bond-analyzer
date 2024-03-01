# CIF Bond Analyzer

This is a codeless and interactive 

## What CIF Bond Anaylzer does

1. processes Crystallographic Information Files (CIF) from selected folder
2. forms supercell based CIF info
3. determines shortest unique atomic pairs found across all CIF files.
4. indicates frequency and distances of bonding pairs.
5. identifies missing atomic pairs not observed across all CIF files.
6. generates histograms for each unique atomic pair to visualize distribution of distances.


When you run `python main.py`, it identifies folders containing `.cif` files.

```
Available folders containing CIF files:
1. binary_files, 3 files
2. backup_cif_files, 1 files
3. 20240229_oliynyk_test_atom_mixing_formatted, 3 files

Enter the number corresponding to the folder containing .cif files: 
```



After processing, it saves `summary_and_missing_pairs.txt` with an exmaple below.

```
Summary:
Pair: Co-Ga, Count: 1, Distances: 2.601
Pair: Ga-Ga, Count: 1, Distances: 2.601
Pair: Ga-La, Count: 1, Distances: 3.291
Pair: In-In, Count: 1, Distances: 2.825
Pair: In-U, Count: 1, Distances: 2.825
Pair: In-Rh, Count: 1, Distances: 2.825
Pair: Rh-U, Count: 1, Distances: 2.825
Pair: Rh-Rh, Count: 1, Distances: 2.825
Pair: Co-Co, Count: 1, Distances: 2.501
Pair: Co-La, Count: 1, Distances: 2.979

Missing pairs:
La-Rh
Co-U
Ga-In
La-U
Co-In
Ga-Rh
In-La
Ga-U
Co-Rh
```


## Installation
Simply copy and paste the following block.

```bash
git clone https://github.com/bobleesj/cif-bond-analyzer.git
cd cif-bond-analyzer
pip install pandas==2.2.1 click==8.1.7 gemmi==0.6.5 matplotlib==3.8.3 pytest==8.0.1
python main.py
```

The above method had no issue so far. But If you are interested in using `Conda` with a fresh new environment

```bash
git clone https://github.com/bobleesj/cif-bond-analyzer.git
cd cif-bond-analyzer
conda create -n cif python=3.10
conda activate cif
pip install -r requirements.txt
python main.py
```

## Tutorial
> If you are new to Conda (Python package manager), I have written a tutorial for you here [Intro to Python package manager for beginners (Ft. Conda with Cheatsheet](https://bobleesj.github.io/tutorial/2024/02/26/intro-to-python-package-manager.html).

## Test
```
python -m pytest           
```

## Contributors
- Anton Oliynyk
- Sangjoon Bob Lee
- Emil Jaffal

## Questions?
Please feel free to reach out via sl5400@columbia.edu for any questions. 

## To-do
- [x] Test shortest distances identified with formatted `1612190.cif`, `539016.cif`
- [ ] Test missing pairs identified
- [ ] Test histogram production
- [ ] Test text file content for binary, ternary, and quartner files. 

## Changelog
- 20240229 - include support for binary, ternary, and quaternary CIF files