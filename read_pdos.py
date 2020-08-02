import numpy as np


def load_doscar_raw_data(path):
    DOSCAR_file = open(path, 'r')
    title = [int(x) for x in DOSCAR_file.readline().split()]
    Natoms = title[0]  # number of atoms (The first number and the second look the same, not sure the difference.)

    for i in range(0, 4):
        DOSCAR_file.readline()  # To skip 4 lines

    (Emax, Emin, NEDOS, Efermi, weight) = [float(x) for x in DOSCAR_file.readline().split()]  # first line of total dos
    NEDOS = int(NEDOS)

    total_dos = []
    for i in range(0, NEDOS):
        total_dos_line = [float(x) for x in DOSCAR_file.readline().split()]
        total_dos.append(total_dos_line)

    total_dos_np = np.array(total_dos)

    energy = total_dos_np[:, 0] - Efermi

    ispin = 1 + int(total_dos_np.shape[1] == 5)  # determine spin polarization

    pdos_raw_data = np.zeros((NEDOS, 1 + ispin * 9, Natoms))

    for j in range(0, Natoms):
        DOSCAR_file.readline()  # skip the first line of pdos (it is the same as total dos)
        for i in range(0, NEDOS):
            pdos_raw_data[i, :, j] = [float(x) for x in DOSCAR_file.readline().split()]
    print(pdos_raw_data.shape)
    return ispin, total_dos_np, Efermi, energy, pdos_raw_data
