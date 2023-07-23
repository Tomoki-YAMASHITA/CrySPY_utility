#!/usr/bin/env python3
#
# pos2pkl.py
#    2023 July 22, T. Yamashita
#        filter option: remove and sort species
#        permit_diff_comp option: permit different composition
#
#    2022 April 9, T. Yamashita
#        convert init_POSCARS, POSCAR, cif to init_struc_data.pkl
#        pymatgen is required
#
import argparse
import os
import pickle
import sys

from pymatgen.core import Structure


def check_append():
    if os.path.isfile('init_struc_data.pkl'):
        print('init_struc_data.pkl already exists.')
        while True:
            choice = input("Append to init_struc_data.pkl? [y/n]: ").lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                print('\nNothing done')
                sys.exit()
    else:
        return False


def read_pos(infile, cid, struc_data, comp, permit_diff_comp, filter):
    tmp_pos = []
    with open(infile, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if 'ID_' in line:
            if tmp_pos:
                tmp_pos = ''.join(tmp_pos)    # line --> str
                tmp_struc = Structure.from_str(tmp_pos, fmt='poscar')
                if filter:    # not vacant
                    tmp_struc = remove_sort(tmp_struc, filter)
                if not permit_diff_comp:
                    if comp is None:
                        comp = tmp_struc.composition
                        print(f'Composition: {comp}')
                    if comp != tmp_struc.composition:
                        print(f'\nError! Composition is different: {infile}')
                        print(f'{comp}    {tmp_struc.composition}')
                        sys.exit()
                struc_data[cid] = tmp_struc
                cid += 1
                tmp_pos = []
                tmp_pos.append(line)    # 1st line for new struc
                continue
            if not tmp_pos:
                tmp_pos.append(line)
        else:
            tmp_pos.append(line)
    if tmp_pos:    # for last structure (no ID_ in next line)
        tmp_pos = ''.join(tmp_pos)    # line --> str
        tmp_struc = Structure.from_str(tmp_pos, fmt='poscar')
        struc_data[cid] = tmp_struc
        cid += 1
    return cid, struc_data, comp


def read_single(infile, cid, struc_data, comp, permit_diff_comp, filter):
    tmp_struc = Structure.from_file(infile)
    if filter:    # not vacant
        tmp_struc = remove_sort(tmp_struc, filter)
    if not permit_diff_comp:
        if comp is None:
            comp = tmp_struc.composition
            print(f'Composition: {comp}')
        if comp != tmp_struc.composition:
            print(f'\nError! Composition is different: {infile}')
            print(f'{comp}    {tmp_struc.composition}')
            sys.exit()
    struc_data[cid] = tmp_struc
    cid += 1
    return cid, struc_data, comp


def remove_sort(struc, filter):
    struc_species = set([x.species_string for x in struc])
    del_ele = struc_species - set(filter)
    if del_ele:
        struc.remove_species(del_ele)
        print(f'Removed species: {del_ele}')
    return struc.get_sorted_structure(key=lambda x: filter.index(x.species_string))

if __name__ == '__main__':
    '''
    convert init_POSCARS, POSCAR, cif to init_struc_data.pkl
    '''
    # ---------- argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file: init_POSCARS', nargs='*')
    parser.add_argument('-s', '--single', help='input file: single structure file (POSCAR, cif)', nargs='*')
    parser.add_argument('-f', '--filter', help='filter (sort): remove species and sort', nargs='*')
    parser.add_argument('-p', '--permit_diff_comp', help='flag for permitting different composition', action='store_true')
    args = parser.parse_args()

    # ---------- if no inputs
    #            ==> args.single: None or []
    if args.single is None:
        args.single = []    # None --> []
    if len(args.infile) == 0 and len(args.single) == 0:
        parser.print_help()
        sys.exit()

    # ---------- initialize
    cid = 0
    struc_data = {}
    natot = 0
    comp = None

    # ---------- check init_struc_data
    append = check_append()

    # ---------- read init_struc_data.pkl
    if append:
        with open('init_struc_data.pkl', 'rb') as f:
            struc_data = pickle.load(f)
        natot = struc_data[0].num_sites
        comp = struc_data[0].composition
        cid = len(struc_data)
        print('\nLoad init_struc_data')
        print(f'Composition: {comp}')
        print(f'The number of structures: {len(struc_data)}')

    # ---------- init_POSCARS --> init_struc_data.pkl
    for x in args.infile:
        cid, struc_data, comp = read_pos(x, cid, struc_data, comp, args.permit_diff_comp, args.filter)

    # ---------- POSCAR, cif --> init_struc_data.pkl
    for x in args.single:
        cid, struc_data, comp = read_single(x, cid, struc_data, comp, args.permit_diff_comp, args.filter)

    # ---------- save
    print(f'\nConverted. The number of structures: {len(struc_data)}')
    with open('init_struc_data.pkl', 'wb') as f:
        pickle.dump(struc_data, f)
    print('Save init_struc_data.pkl')
