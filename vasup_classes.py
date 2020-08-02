from typing import List

import numpy as np


class Orbital:
    s = 0
    py = 1
    pz = 2
    px = 3
    dxy = 4
    dyz = 5
    dz2 = 6
    dxz = 7
    dx2 = 8


class PdosSlice(object):

    def __init__(self, raw_data):
        self.sub_pdos = raw_data

    def get_orbital(self, orbital: int):
        return np.sum(self.sub_pdos[:, orbital, :], 1)


class Pdos(object):

    def __init__(self, raw_data):
        self.pdos = raw_data

    def get_slice(self, start: int, end: int):
        return PdosSlice(self.pdos[:, :, start - 1:end])  # e.g. 1:36,37:37,38:72 becomes
        #      0:36,36:37,37:72


class GraphConfig(object):
    def __init__(self, atoms, color: str, label: str):
        self.atoms = atoms
        self.color = color
        self.label = label


class Drawing(object):

    def __init__(self, pdos_slice, include_orbitals: List[str]):
        self.s_orb = pdos_slice.get_orbital(Orbital.s)
        self.py_orb = pdos_slice.get_orbital(Orbital.py)
        self.pz_orb = pdos_slice.get_orbital(Orbital.pz)
        self.px_orb = pdos_slice.get_orbital(Orbital.px)
        self.dxy_orb = pdos_slice.get_orbital(Orbital.dxy)
        self.dyz_orb = pdos_slice.get_orbital(Orbital.dyz)
        self.dz2_orb = pdos_slice.get_orbital(Orbital.dz2)
        self.dxz_orb = pdos_slice.get_orbital(Orbital.dxz)
        self.dx2_orb = pdos_slice.get_orbital(Orbital.dx2)

        self.p_orb = self.py_orb + self.px_orb + self.pz_orb
        self.d_orb = self.dxy_orb + self.dyz_orb + self.dz2_orb + self.dxz_orb + self.dx2_orb

        self.s_config = GraphConfig(self.s_orb, 'b', 's')
        self.py_config = GraphConfig(self.py_orb, 'g', 'py')
        self.pz_config = GraphConfig(self.pz_orb, 'r', 'pz')
        self.px_config = GraphConfig(self.px_orb, 'c', 'px')
        self.p_config = GraphConfig(self.p_orb, 'r', 'p')
        self.dxy_config = GraphConfig(self.dxy_orb, 'm', 'dxy')
        self.dyz_config = GraphConfig(self.dyz_orb, 'y', 'dyz')
        self.dz2_config = GraphConfig(self.dz2_orb, 'b', 'dz2')
        self.dxz_config = GraphConfig(self.dxz_orb, 'g', 'dxz')
        self.dx2_config = GraphConfig(self.dx2_orb, 'r', 'dx2')
        self.d_config = GraphConfig(self.d_orb, 'c', 'd')

        self.configs = []
        if "s" in include_orbitals:
            self.configs.append(self.s_config)
        if "p" in include_orbitals:
            self.configs.append(self.p_config)
        if "d" in include_orbitals:
            self.configs.append(self.d_config)
        if "px" in include_orbitals:
            self.configs.append(self.px_config)
        if "py" in include_orbitals:
            self.configs.append(self.py_config)
        if "pz" in include_orbitals:
            self.configs.append(self.pz_config)
        if "dxy" in include_orbitals:
            self.configs.append(self.dxy_config)
        if "dyz" in include_orbitals:
            self.configs.append(self.dyz_config)
        if "dz2" in include_orbitals:
            self.configs.append(self.dz2_config)
        if "dxz" in include_orbitals:
            self.configs.append(self.dxz_config)
        if "dx2" in include_orbitals:
            self.configs.append(self.dx2_config)
        if not include_orbitals:
            self.configs = [
                self.s_config,
                self.p_config,
                self.d_config,
            ]
