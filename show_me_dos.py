#!/usr/bin/env python

import argparse
import os
import matplotlib
import matplotlib.pyplot as plt
from read_pdos import load_doscar_raw_data
from vasup_classes import Pdos, Drawing
import numpy as np
import read_poscar
from show_me_dos_main import show_me_dos_function

# https://docs.python.org/3/library/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='path: default $PWD', required=False)
parser.add_argument('-d', '--DOSCAR_name_input', help='default DOSCAR', required=False)

# TODO: SS  fix minus sign problem, now I have to use -xy="-10:10,0:300"  as input
parser.add_argument('-xy', '--xyrange', help='DOS plot x axis range format:xa:xb,ya:yb', type=str, required=False)
parser.add_argument('-s', '--size', help='figure size a,b', type=str, required=False)

parser.add_argument('-a', '--atoms', help='atoms range a:b, or just a number', type=str, required=False)
parser.add_argument('-f', '--factor', help='fator a,b,c,d ..  match the atoms group', type=str, required=False)
parser.add_argument('--colors', help='colors a,b,c,d ..  match the atoms group', type=str, required=False)
parser.add_argument('-o', '--orbital', help='draw certain orbital', type=str, default="s|p|d", required=False)
parser.add_argument('--notsave', help="not save the plot", action="store_true")
parser.add_argument('--nosize', help="not change figure size", action="store_true")
parser.add_argument('--notshow', help="not show the plot", action="store_true")
parser.add_argument('--pdf', help="save the plot in pdf", action="store_true")
parser.add_argument('--absolute', help="absolute energy scales", action="store_true")


# TODO: Homework - SS - add a parameter split=true/false to split orbital into multiple ones
# TODO: SS  turn off total DOS
# TODO: selectively turn off s,p,d orbital..
# TODO: time factor in label
# TODO: color scheme
args = parser.parse_args()

include_orbitals = args.orbital.split("|")

# https://stackoverflow.com/a/5137509/1035008
if args.input:
    currentFolder = args.input
else:
    currentFolder = os.getcwd()

if args.DOSCAR_name_input:
    DOSCAR_name = "/" + args.DOSCAR_name_input
else:
    DOSCAR_name = "/DOSCAR"

DOSCAR_path = currentFolder + DOSCAR_name
POSCAR_path = currentFolder + "/POSCAR"

atom_ranges = []

if args.atoms:
    for atom_range in args.atoms.split(','):
        if ':' in atom_range:
            start, end = atom_range.split(":")
            atom_ranges.append((int(start), int(end))) # debug
        else:
            atom_ranges.append((int(atom_range), int(atom_range)))
else:
    atom_ranges = read_poscar.read_atom_number(POSCAR_path)
print('Atoms range are {}'.format(atom_ranges))


factors = []
if args.factor:
    for fac_tor in args.factor.split(','):
        factors.append(fac_tor)

else:
    factors = np.ones(len(atom_ranges))

print('Scale factors are {}'.format(factors))

border_colors = []
if args.colors:
    border_colors = args.colors.split(',')
else:
    border_colors = ['darkblue', 'darkred', 'darkgreen', '#ff9900', '#9999ff', '#996633', '#00ffff', '#003300']




size_figure = []
if args.size:
    for si_ze in args.size.split(','):
        size_figure.append(float(si_ze))
else:
    size_figure = [8, 5]
print('size are {}'.format(size_figure))



if args.xyrange:
    xrange, yrange = args.xyrange.split(',')
    xlim1, xlim2 = [float(x) for x in xrange.split(":")]
    ylim1, ylim2 = [float(x) for x in yrange.split(":")]


else:
    xlim1, xlim2 = [-10, 10]
    ylim1, ylim2 = [-200, 200]

notsave = args.notsave
notshow = args.notshow
pdf     = args.pdf
nosize = args.nosize

absolute = args.absolute

show_me_dos_function(DOSCAR_path, POSCAR_path,xlim1, xlim2, ylim1, ylim2,border_colors,factors,atom_ranges,size_figure,include_orbitals,notsave,notshow,pdf,nosize,absolute)
