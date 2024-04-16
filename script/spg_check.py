#!/usr/bin/env python

import argparse

from pymatgen.core import Structure


def get_spg_info(filename, tolerance=0.01):
    struc = Structure.from_file(filename)
    spg_sym, spg_num = struc.get_space_group_info(symprec=tolerance)
    return spg_sym, spg_num


if __name__ == '__main__':
    # ---------- argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tolerance', help='tolerance', type=float, default=0.01)
    parser.add_argument('infile', help='input file')
    args = parser.parse_args()

    # ---------- main
    print(get_spg_info(args.infile, args.tolerance))
