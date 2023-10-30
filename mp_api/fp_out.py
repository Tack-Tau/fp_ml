#!/usr/bin/env python3

import os
import sys
import numpy as np
import pickle
from functools import reduce
import fplib3
import ase.io

# cell_file = 'POSCAR'

def get_fp_mat(cell_file):
    atoms = ase.io.read('.'+'/'+cell_file)
    Nat = len(atoms)
    # print("Number of atoms:", Nat)

    lat = atoms.cell[:]
    rxyz = atoms.get_positions()
    chem_nums = list(atoms.numbers)
    znucl_list = reduce(lambda re, x: re+[x] if x not in re else re, chem_nums, [])
    ntyp = len(znucl_list)
    znucl = np.array(znucl_list, int)

    default_parameters = {
                          'cutoff': 6.0,
                          'contract': False,
                          'znucl': znucl,
                          'lmax': 0,
                          'nx': 300,
                          'ntyp': ntyp
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

    # fp_flat = fp.reshape((int(len(fp)/Nat)), nx*Nat).ravel()
    fp_mat = np.float64(fp)

    # fpe = fplib3.get_fpe(fp_mat, ntyp = ntyp, types = types)
    # fp_energy_per_atom = float( fpe / len(atoms) )

    # np.set_printoptions(threshold=sys.maxsize)

    # print("Fingerprint energy per atom is \n{0:.6f}".format(fp_energy_per_atom))
    # print("Fingerprint matrix is\n", repr(fp_mat))
    
    return fp_mat

if __name__ == "__main__":
    current_dir = './'
    Nat_max = 0
    mpid_fp_dict = {}
    for filename in os.listdir(current_dir):
        f = os.path.join(current_dir, filename)
        if os.path.isfile(f) and f.split('/')[1].split('_')[0] == 'POSCAR':
            cell_file = f.split('/')[1]
            atoms = ase.io.read('.'+'/'+cell_file)
            Nat_tmp = len(atoms)
            if Nat_tmp >= Nat_max:
                Nat_max = Nat_tmp
            # mat_id = cell_file.split('.')[0].split('_')[1]
            # print(cell_file, mat_id)
            # mpid_fp_mat_dict[str(mat_id)] = get_fp_mat(cell_file)
    # print(Nat_max)
    for filename in os.listdir(current_dir):
        f = os.path.join(current_dir, filename)
        if os.path.isfile(f) and f.split('/')[1].split('_')[0] == 'POSCAR':
            cell_file = f.split('/')[1]
            mat_id = cell_file.split('.')[0].split('_')[1]
            fp_mat = get_fp_mat(cell_file)
            nx = len(fp_mat[0])
            fp_pad = np.zeros((Nat_max, nx), dtype = float)
            fp_pad[:fp_mat.shape[0], :fp_mat.shape[1]] = fp_mat
            fp_flat = fp_pad.reshape((int(len(fp_pad)/Nat_max)), nx*Nat_max).ravel()
            # print(fp_pad.shape)
            mpid_fp_dict[str(mat_id)] = np.float64(fp_flat)
            
    with open('mpid_fp_info.pkl', 'wb') as f:
        pickle.dump(mpid_fp_dict, f)
        print('Dictionary saved successfully to file')
