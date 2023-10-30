#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import collections
import pickle
from mp_api.client import MPRester

MP_API_KEY=os.environ.get("MP_API_KEY")

'''
with MPRester(MP_API_KEY) as mpr:
    """
    # print("mpr.materials.available_fields:\n", mpr.materials.available_fields)
    # print("mpr.materials.summary.available_fields:\n", mpr.summary.available_fields)
    # print("mpr.thermo.available_fields:\n", mpr.thermo.available_fields)
    # print("mpr.get_entries_in_chemsys.available_fields:\n", mpr.get_entries_in_chemsys.available_fields)
    print("dir(mpr.materials):\n", dir(mpr.materials))
    print("dir(mpr.materials.summary):\n", dir(mpr.materials.summary))
    print("dir(mpr.get_entries_in_chemsys):\n", dir(mpr.get_entries_in_chemsys))
    print("dir(mpr.materials.get_data_by_id):\n", dir(mpr.materials.get_data_by_id))
    """
    docs = mpr.materials.summary.search(
        chemsys=["Na", "Si", "Ge", "Na-Si", "Na-Ge", "Si-Ge"], fields=["material_id", "is_metal", "is_gap_direct", "band_gap", "formula_pretty", "calc_types"]
    )
    mpid_bgap_dict = {
        doc.formula_pretty:
        {"Material ID": doc.material_id,
         "Metality": doc.is_metal,
         "Direct or not": doc.is_gap_direct,
         "Gap value (eV)": doc.band_gap,
         # "Calculation types": mpr.materials.get_data_by_id(doc.material_id, fields = ["calc_types"]).calc_types
        }
        for doc in docs
    }
    # sorted_mpid_bgap_dict = dict(sorted(mpid_bgap_dict.items()))
    # sorted_mpid_bgap_dict = dict( collections.OrderedDict( sorted( mpid_bgap_dict.items() ) ) )
    # print(sorted_mpid_bgap_dict)
    for key1 in mpid_bgap_dict:
        for key2 in mpid_bgap_dict:
            if (key1 == key2) and \
            (mpid_bgap_dict[key1]["Material ID"] != mpid_bgap_dict[key2]["Material ID"]):
                print(key1, mpid_bgap_dict[key1])
                print(key2, mpid_bgap_dict[key2])
'''

with MPRester(MP_API_KEY) as mpr:
    entries = mpr.get_entries_in_chemsys(elements=["C", "N", "B", "O", "Si"])
    # data = collections.defaultdict(list)
    mat_id_list = []
    for e in entries:
        comp = e.composition
        chem_form = comp.reduced_formula
        e_id = e.entry_id
        mat_id = '-'.join( [ e_id.split('-')[0], e_id.split('-')[1] ] )
        mat_id_list.append( mat_id )
        struct = mpr.get_structure_by_material_id(mat_id)
        struct.to('POSCAR' + '_' + str(mat_id) + '.vasp', fmt='POSCAR')
        
    # print("mat_id_list:\n", mat_id_list)
    docs = mpr.materials.summary.search(
        material_ids = mat_id_list,
        fields = ["material_id", "is_metal", "is_gap_direct", "band_gap", "formula_pretty", "calc_types"]
    )
    mpid_bgap_dict = {
        str(doc.material_id):
        {"Metality": bool(doc.is_metal),
         "Direct or not": bool(doc.is_gap_direct),
         "Gap value (eV)": float(doc.band_gap),
         # "Calculation types": mpr.materials.get_data_by_id(doc.material_id, fields = ["calc_types"]).calc_types
        }
        for doc in docs
    }
    # sorted_mpid_bgap_dict = dict(sorted(mpid_bgap_dict.items()))
    # sorted_mpid_bgap_dict = dict( collections.OrderedDict( sorted( mpid_bgap_dict.items() ) ) )
    # print(sorted_mpid_bgap_dict)
    # print(mpid_bgap_dict)
    
    with open('mpid_bgap_info.pkl', 'wb') as f:
        pickle.dump(mpid_bgap_dict, f)
        print('Dictionary saved successfully to file')