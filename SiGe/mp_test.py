#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pickle

mpid_bgap_dict = {}

with open('mpid_bgap_list', 'rb') as f:
    for line in f:
        mat_id_str = line.decode().split()[0]
        metality_str = line.decode().split()[1]
        E_gap_str = line.decode().split()[2]
        
        is_metal = bool( metality_str=='Metallic' or  metality_str=='Semimetallic' )
        is_gap_direct = bool( metality_str=='Direct' )
        E_gap = float(E_gap_str)
        mpid_bgap_dict[str(mat_id_str)] = {"Metality": is_metal,
                                           "Direct or not": is_gap_direct,
                                           "Gap value (eV)": E_gap
                                          }

# print(mpid_bgap_dict)

with open('mpid_bgap_info.pkl', 'wb') as f:
    pickle.dump(mpid_bgap_dict, f)
    print('Dictionary saved successfully to file')