#!/usr/bin/env python3
#
# get_primitive_cell.py
#   2022/03/08 T. Yamashita
#   get primitive cell using pymatgen
#     - pymatgen is required
#     - input: cif, POSCAR, xxx.vasp, etc. (readable file in pymatgen)
#     - output: standrd output. POSCAR format.
#   example
#     python3 get_primitive_cell abc.cif > POSCAR
#
import argparse

from pymatgen.core import Structure


def get_primitive(infile):
    struc = Structure.from_file(infile)
    # ---------- to primitive
    struc = struc.get_primitive_structure()
    # ---------- output
    print(struc.to(fmt='poscar'))

if __name__ == '__main__':
    # ---------- argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file')
    args = parser.parse_args()

    # ---------- main
    get_primitive(args.infile)
