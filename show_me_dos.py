#!/usr/bin/env python

import argparse
import os
import matplotlib
import matplotlib.pyplot as plt
from read_pdos import load_doscar_raw_data
from vasup_classes import Pdos, Drawing
import numpy as np
import read_poscar

# https://docs.python.org/3/library/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='path: default $PWD', required=False)
parser.add_argument('-d', '--DOSCAR_name_input', help='default DOSCAR', required=False)

# TODO: SS  fix minus sign problem, now I have to use -xy="-10:10,0:300"  as input
parser.add_argument('-xy', '--xyrange', help='DOS plot x axis range format:xa:xb,ya:yb', type=str, required=False)
parser.add_argument('-s', '--size', help='figure size a,b', type=str, required=False)

parser.add_argument('-a', '--atoms', help='atoms range a:b, or just a number', type=str, required=False)
parser.add_argument('-f', '--factor', help='fator a,b,c,d ..  match the atoms group', type=str, required=False)

parser.add_argument('-o', '--orbital', help='draw certain orbital', type=str, default="s|p|d", required=False)

# TODO: Homework - SS - add a parameter split=true/false to split orbital into multiple ones
# TODO: SS  turn off total DOS
# TODO: selectively turn off s,p,d orbital..
# TODO: time factor ...
# TODO: color scheme
# TODO: automatically get atomic number from POSCAR if POSCAR existed
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

ispin, total_dos_np, Efermi, energy, pdos_raw_data = load_doscar_raw_data(path=DOSCAR_path)

def plot_total(energy0, total_dos, label=None):
    plt.plot(energy0, total_dos, color='black', linewidth=1, alpha=0.5, label=label)



pdos_list = []

plot_total(energy, total_dos_np[:, 1], "Total DOS")

if ispin == 1:
    pdos = Pdos(raw_data=pdos_raw_data[:, 1:])
    pdos_list = [pdos]
elif ispin == 2:
    plot_total(energy, -total_dos_np[:, 2])
    pdos_1 = Pdos(raw_data=pdos_raw_data[:, 1::2])
    pdos_2 = Pdos(raw_data=-pdos_raw_data[:, 2::2])
    pdos_list = [pdos_1, pdos_2]



# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.colors.html
border_colors = ['#000099', 'red', 'chartreuse', '#ff9900','#9999ff','#996633','#00ffff','#003300']
elements_label, elements_array = read_poscar.read_element(POSCAR_path)

for num, pdos in enumerate(pdos_list):
    for index1, atom_range in enumerate(atom_ranges):
        #print('this is index 1:  {}'.format(index1))
        pdos_slice = pdos.get_slice(start=atom_range[0], end=atom_range[1])
        drawing = Drawing(pdos_slice, include_orbitals=include_orbitals)
        #atom_label = "atom{}: {}".format(index1 + 1, atom_range)
        border_color = border_colors[index1]

        for index2, config in enumerate(drawing.configs):
            #print('the config is: {}'.format(config))
            #print('this is index 2:  {}'.format(index2))
            #print(factors[index1])
            plt.fill_between(
                energy,
                0,
                config.atoms * int(factors[index1]),
                color=config.color,
                linewidth=1,
                alpha=0.5,
                label=config.label if (index1 == 0 and num == 1) else None
            )

            starting_with = 0
            resolve_label = ""
            for i, a in enumerate(elements_array):
                if starting_with < atom_range[0] <= starting_with + a:
                    resolve_label = elements_label[i]
                    break
                starting_with += a  # 3, 6, 12


            plt.plot(
                energy,
                config.atoms*int(factors[index1]),
                color=border_color,
                linewidth=1,
                label=resolve_label if (index2 == 0 and num == 1) else None
            )

plt.xlim(xlim1, xlim2)
plt.ylim(ylim1, ylim2)
plt.xlabel(r'E - E$_f$ (eV)', fontsize=16)
plt.ylabel('PDOS (a.u.)', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.axvline(x=0, color='k', linestyle='--')

lgd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True, ncol=8)




fig = matplotlib.pyplot.gcf()
fig.set_size_inches(size_figure[0], size_figure[1], forward=True)

plt.savefig('PDOS.pdf', bbox_extra_artists=[lgd], bbox_inches='tight')
plt.show()

