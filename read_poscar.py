import numpy as np


def read_atom_number(filepath):
    """read CONTCAR/POSCAR and output basis vectors, elements, number of atoms1 and atom2 and whole coordinates"""
    input_file = open(filepath, 'r')
    _ = input_file.readline()
    _ = input_file.readline()
    _ = input_file.readline()
    _ = input_file.readline()
    _ = input_file.readline()

    elements = np.array([x for x in input_file.readline().split()])
    number_of_atoms = [int(x) for x in input_file.readline().split()]  # e.g. 72 72

    left = 1
    right = 0

    atom_ranges = []
    for i in range(0, len(number_of_atoms)):
        left = right + 1
        right = right + number_of_atoms[i]
        atom_ranges.append((left, right))

    return atom_ranges


def read_element(filepath):
    """read CONTCAR/POSCAR and output basis vectors, elements, number of atoms1 and atom2 and whole coordinates"""
    input_file = open(filepath, 'r')
    _ = input_file.readline()
    _ = input_file.readline()
    _ = input_file.readline()
    _ = input_file.readline()
    _ = input_file.readline()

    elements_label = np.array([x for x in input_file.readline().split()])
    elements_array = np.array([int(x) for x in input_file.readline().split()])

    return elements_label, elements_array
