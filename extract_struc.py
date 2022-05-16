#!/usr/bin/env python3
#
# extract_struc.py
#
#   2022/05/15 T. Yamashita
#   --all option
#
#   2020/05/26 T. Yamashita
#   extract a structure from init_struc_data.pkl or opt_struc_data.pkl
#   pymatgen is required
#
import argparse
import pickle


if __name__ == '__main__':
    '''
    extract a structure/structures from init_struc_data.pkl or opt_struc_data.pkl
    and output cif file(s)

    example:
    - write cifs of ID 7 10 12 (output 7.cif, 10.cif, 12.cif)
      python3 extract_struc.py init_struc_data.pkl -i 7 10 12

    - write cifs of ID 7 10 12 (output 7.cif, 10.cif, 12.cif) with symmetry information
      python3 extract_struc.py init_struc_data.pkl -i 7 10 12 -s

    - write all (output 0.cif, 1.cif, 2.cif ....)
      python3 extract_struc.py init_struc_data.pkl -a

    - write all (output 0.cif, 1.cif, 2.cif ....) with symmetry information
      python3 extract_struc.py init_struc_data.pkl -as
    '''
    # ---------- argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all_id', help='flag for all structures', action='store_true')
    parser.add_argument('-i', '--index', help='structure ID', type=int, nargs='*')
    parser.add_argument('-s', '--symmetrized', help='flag for symmetrized structure', action='store_true')
    parser.add_argument('infile', help='input file')
    args = parser.parse_args()

    # ---------- load struc_data
    with open(args.infile, 'rb') as f:
        struc_data = pickle.load(f)

    # ---------- write cif
    if args.index:   # not vacant
        for cid in args.index:
            if args.symmetrized:
                struc_data[cid].to(fmt='cif', filename='{}.cif'.format(cid), symprec=0.1)
            else:
                struc_data[cid].to(fmt='cif', filename='{}.cif'.format(cid))
        raise SystemExit()

    # ---------- all
    if args.all_id:
        for cid, struc in struc_data.items():
            if args.symmetrized:
                struc.to(fmt='cif', filename='{}.cif'.format(cid), symprec=0.1)
            else:
                struc.to(fmt='cif', filename='{}.cif'.format(cid))
