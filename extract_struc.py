#!/usr/bin/env python3
#
# extract_struc.py
#   2020/05/26 T. Yamashita
#   extract a structure from init_struc_data.pkl or opt_struc_data.pkl
#   pymatgen is required
#
import argparse
import pickle

from pymatgen.io.cif import CifWriter


def get_struc(infile, cid):
    with open(infile, 'rb') as f:
        struc_dict = pickle.load(f)
    return struc_dict[cid]


if __name__ == '__main__':
    '''
    extract a structure from init_struc_data.pkl or opt_struc_data.pkl
    and output cif file
    '''
    # ---------- argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--symmetrized', help='flag for symmetrized structure', action='store_true')
    parser.add_argument('infile', help='input file')
    parser.add_argument('cid', help='structure ID', type=int)
    args = parser.parse_args()

    # ---------- get structure
    struc = get_struc(args.infile, args.cid)

    # ---------- write cif
    if args.symmetrized:
        cw = CifWriter(struc, symprec=0.1)
    else:
        cw = CifWriter(struc, symprec=None)
    cw.write_file('{}.cif'.format(args.cid))
