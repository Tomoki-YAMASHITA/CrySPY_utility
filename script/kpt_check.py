#!/usr/bin/env python3
#
# kpt_check.py
#     2024/04/21 quit MITRelaxSet, just use Kpoints class, T. Yamashita
#     2021/06/25 modified for new style of pymatgen, T. Yamashita
#     20??/??/?? T. Yamashita
#
import argparse
import pickle

from pymatgen.core import Structure
from pymatgen.io.vasp import Kpoints


def get_struc(filepath):
    struc = Structure.from_file(filepath)
    return struc


def load_init_struc(filepath):
    with open(filepath, 'rb') as dstruc:
        init_struc_data = pickle.load(dstruc)
    return init_struc_data


def write_kpt(struc, kppvol):
    kpoints = Kpoints.automatic_density_by_vol(structure=struc, kppvol=kppvol)
    kpoints.write_file('KPOINTS')


def kpt_check(struc, kppvol):
    kpoints = Kpoints.automatic_density_by_vol(structure=struc, kppvol=kppvol)
    print('a =', struc.lattice.a)
    print('b =', struc.lattice.b)
    print('c =', struc.lattice.c)
    print('    Lattice vector')
    print(struc.lattice)
    print()
    print('kppvol: ', kppvol)
    print('k-points: ', kpoints.kpts[0])


def kpt_check_init_struc(init_struc_data, kppvol, nstruc):
    init_struc_data = [init_struc_data[i] for i in range(len(init_struc_data))]    # dict --> list
    for cnt, struc in enumerate(init_struc_data):
        print('\n\n# ---------- {}th structure'.format(cnt))
        kpt_check(struc, kppvol)
        if cnt == nstruc-1:
            return
    return


if __name__ == '__main__':
    '''
    sys.argv[1] <-- POSCAR, CONTCAR, or init_struc_data.pkl
    sys.argv[2] <-- kppvol
    '''
    # ---------- argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--write', help='write KPOINTS', action='store_true')
    parser.add_argument('-n', '--nstruc', help='number of structure to check', type=int, default=5)
    parser.add_argument('infile', help='input file: POSCAR, CONTCAR, or init_struc_data.pkl')
    parser.add_argument('kppvol', help='kppvol', type=int)
    args = parser.parse_args()

    # ---------- main
    vaspfiles = ['POSCAR', 'CONTCAR']
    filename = args.infile.split('/')[-1]
    if filename in vaspfiles:
        struc = get_struc(args.infile)
        if args.write:
            write_kpt(struc, args.kppvol)
        else:
            kpt_check(struc, args.kppvol)
    elif filename == 'init_struc_data.pkl':
        init_struc_data = load_init_struc(args.infile)
        kpt_check_init_struc(init_struc_data, args.kppvol, args.nstruc)
    else:
        raise SystemExit('usage: kpt_check.py [-h] [-w] [-n NSTRUC] infile kppvol')
