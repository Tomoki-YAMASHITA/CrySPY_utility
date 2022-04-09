#!/usr/bin/env python3
#
# extract_struc.py
#   2022 April 9 T. Yamashita
#   convert init_POSCARS, POSCAR, cif to init_struc_data.pkl
#   pymatgen is required
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


def read_pos(infile, cid, struc_data, natot):
    tmp_pos = []
    with open(infile, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if 'ID_' in line:
            if tmp_pos:
                tmp_pos = ''.join(tmp_pos)    # line --> str
                tmp_struc = Structure.from_str(tmp_pos, fmt='poscar')
                if natot == 0:
                    natot = tmp_struc.num_sites
                if natot != tmp_struc.num_sites:
                    print('\nNumber of atoms is different!')
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
    return cid, struc_data


def read_single(infile, cid, struc_data, natot):
    tmp_struc = Structure.from_file(infile)
    if natot == 0:
        natot = tmp_struc.num_sites
    if natot != tmp_struc.num_sites:
        print('\nNumber of atoms is different!')
        sys.exit()
    struc_data[cid] = tmp_struc
    cid += 1
    return cid, struc_data


if __name__ == '__main__':
    '''
    convert init_POSCARS, POSCAR, cif to init_struc_data.pkl
    '''
    # ---------- argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file: init_POSCARS', nargs='*')
    parser.add_argument('-s', '--single', help='input file: single structure file (POSCAR, cif)', nargs='*')
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

    # ---------- check init_struc_data
    append = check_append()

    # ---------- read init_struc_data.pkl
    if append:
        with open('init_struc_data.pkl', 'rb') as f:
            struc_data = pickle.load(f)
        natot = struc_data[0].num_sites
        cid = len(struc_data)
        print('\nLoad init_struc_data. The number of structures: {}'.format(len(struc_data)))

    # ---------- init_POSCARS --> init_struc_data.pkl
    for x in args.infile:
        cid, struc_data = read_pos(x, cid, struc_data, natot)

    # ---------- POSCAR, cif --> init_struc_data.pkl
    for x in args.single:
        cid, struc_data = read_single(x, cid, struc_data, natot)

    # ---------- save
    print('\nConverted. The number of structures: {}'.format(len(struc_data)))
    with open('init_struc_data.pkl', 'wb') as f:
        pickle.dump(struc_data, f)
    print('Save init_struc_data.pkl')
