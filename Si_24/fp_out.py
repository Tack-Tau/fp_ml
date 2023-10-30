#!/usr/bin/env python3

import os
import sys
import numpy as np
import fplib3
import ase.io

cell_file = 'POSCAR'
atoms = ase.io.read('.'+'/'+cell_file)
# print("Number of atoms:", len(atoms))

lat = atoms.cell[:]
rxyz = atoms.get_positions()

default_parameters = {
                      'cutoff': 6.0,
                      'contract': False,
                      'znucl': np.array([32, 14], int),
                      'lmax': 0,
                      'nx': 300,
                      'ntyp': 1
                      }

lat = np.array(lat, dtype = np.float64)
rxyz = np.array(rxyz, dtype = np.float64)
types = np.int32(fplib3.read_types(cell_file))
znucl =  np.int32(default_parameters['znucl'])
contract = default_parameters['contract']
ntyp =  np.int32(default_parameters['ntyp'])
nx = np.int32(default_parameters['nx'])
lmax = np.int32(default_parameters['lmax'])
cutoff = np.float64(default_parameters['cutoff'])

fp, _ = fplib3.get_fp(lat, rxyz, types, znucl,
                      contract = contract,
                      ldfp = False,
                      ntyp = ntyp,
                      nx = nx,
                      lmax = lmax,
                      cutoff = cutoff)

fp_mat = np.float64(fp)

# fpe = fplib3.get_fpe(fp_mat, ntyp = ntyp, types = types)
# fp_energy_per_atom = float( fpe / len(atoms) )

# np.set_printoptions(threshold=sys.maxsize)

# print("Fingerprint energy per atom is \n{0:.6f}".format(fp_energy_per_atom))
# print("Fingerprint matrix is\n", repr(fp_mat))

np.savetxt('log', fp_mat, delimiter=',')

