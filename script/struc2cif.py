#!/usr/bin/env python
#
# 2023 Nov. 30 modified by T. Yamashita
#
import argparse

from pymatgen.core import Structure


def get_cif(filename, tolerance=0.01):
    struc = Structure.from_file(filename)
    struc.to(fmt='cif', filename=filename+'.cif', symprec=tolerance)


if __name__ == '__main__':
    # ---------- argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tolerance', help='tolerance', type=float, default=0.01)
    parser.add_argument('infile', help='input file')
    args = parser.parse_args()

    # ---------- main
    filename = args.infile.split('/')[-1]    # ./aaa/bbb/POSCAR --> POSCAR
    get_cif(filename, args.tolerance)
