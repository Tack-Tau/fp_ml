# ML tool for Fingerprint library ([fplib3](https://github.com/Tack-Tau/fplib3))
### Implemented in Python3

## Dependencies
* Python >= 3.8.5
* Numpy >= 1.21.4
* Scipy >= 1.8.0
* Numba >= 0.56.2
* ASE >= 3.22.1
* pymatgen >= v2023.9.10
* mp-api >= 0.37.0

## Setup
For pymatgen documentation please visit their [website](https://pymatgen.org/)\
For ASE documentation: see details for [ASE calculator class](https://wiki.fysik.dtu.dk/ase/development/calculators.html)
and [ASE calculator proposal](https://wiki.fysik.dtu.dk/ase/development/proposals/calculators.html#aep1)\
`conda create -n fplibenv python=3.8 pip ; conda activate fplibenv`\
`python3 -m pip install --user pip setuptools wheel`\
`python3 -m pip install --user numpy scipy ase numba pymatgen mp-api`\
`git clone https://github.com/Tack-Tau/fp_ml.git ./fplib3_ml`

## Usage
### Basic ML with fp as descriptor
See [Si_24](https://github.com/Tack-Tau/fp_ml/tree/master/Si_24) for example

### ML with fp and interfacing with MP-API
See [mp_api](https://github.com/Tack-Tau/fp_ml/tree/master/mp_api) for example