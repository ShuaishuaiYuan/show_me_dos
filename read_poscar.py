import numpy as np

def read_relaxed_data_v3(relax_file):
    "read CONTCAR/POSCAR and output basis vectors, elements, number of atoms1 and atom2 and whole coordinates"
    "I updated the cell vector and the length of a b c"
    input = open(relax_file, 'r')

    line = input.readline()  # 1 Na Cl
    line = input.readline()  # 2 1
    a_vector = np.array([float(x) for x in input.readline().split()] ) # 3
    b_vector = np.array([float(x) for x in input.readline().split()] )# 4
    c_vector = np.array([float(x) for x in input.readline().split()] ) # 5
    cell_vector = np.concatenate((a_vector,b_vector,c_vector), axis=0).reshape(3,3)
    line = input.readline()  # 6 Na Cl
    number_of_atoms_vector = [int(x) for x in input.readline().split()]  # e.g. 72 72
    number_of_atoms = int(np.sum(number_of_atoms_vector))
    line = input.readline()  # Direct # Direct

    data_0 = np.zeros([number_of_atoms, 3])
    # if it does not meet atom positions, this will
    for i in range(number_of_atoms):
        atom = [float(x) for x in input.readline().split()]
        data_0[i, :] = atom
    x_size = np.linalg.norm(a_vector)
    y_size = np.linalg.norm(b_vector)
    z_size = np.linalg.norm(c_vector)
    return data_0, number_of_atoms, x_size, y_size, z_size, number_of_atoms_vector,cell_vector

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
