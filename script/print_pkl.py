#!/usr/bin/env python3
#
# print_pkl.py
#
#   yyyy/mm/dd
#   2024/??/?? T. Yamashita
#
import argparse
import gzip
from pathlib import Path
import pickle
from pprint import pprint


def extract_pkl_name(filepath):
    path = Path(filepath)
    filename = path.name
    if filename.endswith('.gz'):
        filename = Path(filename).stem
    return filename


def out_input(rin):
    print('[basic]')
    for key in rin.__annotations__.keys():
        if key == 'struc_mode':
            print('')
            print('[structure]')
        if key == 'stop_chkpt':
            print('')
            print('[option]')
        if rin.algo == 'BO' and key == 'nselect_bo':
            print('')
            print('[BO]')
        if rin.algo == 'LAQA' and key == 'nselect_laqa':
            print('')
            print('[LAQA]')
        if rin.algo in ['EA', 'EA-vc'] and key == 'n_pop':
            print('')
            print('[EA]')
        if rin.calc_code == 'VASP' and key == 'kpt_flag':
            print('')
            print('[VASP]')
        if rin.calc_code == 'QE' and key == 'kpt_flag':
            print('')
            print('[QE]')
        if rin.calc_code == 'OMX' and key == 'kpt_flag':
            print('')
            print('[OMX]')
        if rin.calc_code == 'soiap' and key == 'kpt_flag':
            print('')
            print('[soiap]')
        if rin.calc_code == 'LAMMPS' and key == 'kpt_flag':
            print('')
            print('[LAMMPS]')
        if rin.calc_code == 'ASE' and key == 'kpt_flag':
            print('')
            print('[ASE]')
        if rin.calc_code == 'ext' and key == 'kpt_flag':
            print('')
            print('[ext]')
        if getattr(rin, key) is not None:
            print(f'{key} = {getattr(rin, key)}')


if __name__ == '__main__':
    '''
    print pkl_data
    '''
    # ---------- argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file')
    args = parser.parse_args()

    # ---------- extract pkl_name
    #     e.g.
    #     ./data/pkl_data/init_struc_data.pkl --> init_struc_data.pkl
    #     ./data/pkl_data/init_struc_data.pkl.gz --> init_struc_data.pkl
    pkl_name = extract_pkl_name(args.infile)

    # ---------- load pkl data
    if args.infile.endswith('.gz'):
        with gzip.open(args.infile, 'rb') as f:
            pkl_data = pickle.load(f)
    else:
        with open(args.infile, 'rb') as f:
            pkl_data = pickle.load(f)

    # ---------- print pkl data
    if pkl_name in [
            'id_queueing.pkl',
            'id_running.pkl',
            'rslt_data.pkl',
            'energy_step_data.pkl',
            'force_step_data.pkl',
            'stress_step_data.pkl',
            # ------ EA
            'gen.pkl',
            'ea_info.pkl',
            'ea_origin.pkl',
            'elite_fitness.pkl',
            # ------ EA-vc
            'nat_data.pkl',
            'ratio_data.pkl',
            'hdist_data.pkl',
            # ------ BO
            'n_selection.pkl',
            'id_select_hist.pkl',
            'bo_mean.pkl',
            'bo_var.pkl',
            'bo_score.pkl',
            # ------ LAQA
            'tot_step_select.pkl',
            'laqa_energy.pkl',
            'laqa_bias.pkl',
            'laqa_score.pkl',
            'laqa_step.pkl',
            'laqa_struc.pkl',
        ]:
        pprint(pkl_data)

    if pkl_name in [
            'init_struc_data.pkl',
            'opt_struc_data.pkl',
            'struc_step_data.pkl',
            'elite_struc.pkl',
            'init_dscrpt_data.pkl',
            'opt_dscrpt_data.pkl',
        ]:
        print(f'Number of structures: {len(pkl_data)}')
        pprint(pkl_data.keys())

    if pkl_name in ['input_data.pkl']:
        out_input(pkl_data)
