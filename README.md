# CIF Bond Analyzer

The code is currently in infancy stage. More updates will be provided. 

## To-do
- [x] Test shortest distances identified with formatted `1612190.cif`, `539016.cif`
- [ ] Test missing shortest distances identified
- [ ] Test histogram production
- [ ] Test overall text file content as final output for binary, ternary, and quartner files. 

## What CIF Bond Anaylzer does
- Identifies shortest bonding pairs across the entire CIF files in the selected folder by the user. 
- Identifies pairs that are not present under the Missing pairs: section
- Saves a txt file at the end of the run in the CIF folder shown below.

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
}

## Installation
Simply copy and paste the following block.

```bash
git clone https://github.com/bobleesj/cif-cleaner.git
cd cif-bond-analyzer
pip install pandas==2.2.1 click==8.1.7 gemmi==0.6.5 matplotlib==3.8.3 pytest==8.0.1
python main.py
```

The above method had no issue so far. But If you are interested in using `Conda` with a fresh new environment

```bash
git clone https://github.com/bobleesj/cif-cleaner.git
cd cif-analyzer
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

## Tutorial
> If you are new to Conda (Python package manager), I have written a tutorial for you here [Intro to Python package manager for beginners (Ft. Conda with Cheatsheet](https://bobleesj.github.io/tutorial/2024/02/26/intro-to-python-package-manager.html).


## Contributors
- Anton Oliynyk
- Sangjoon Bob Lee
- Emil Jaffal

## Questions?
Please feel free to reach out via sl5400@columbia.edu for any questions. If you encounter any issues or bugs, please share them as well.
