import matplotlib
import matplotlib.pyplot as plt
import read_poscar
from read_pdos import load_doscar_raw_data
from vasup_classes import Pdos, Drawing

def show_me_dos_function(DOSCAR_path, POSCAR_path,xlim1, xlim2, ylim1, ylim2,border_colors,factors,atom_ranges,size_figure,include_orbitals, notsave,notshow,pdf,nosize,absolute):
    """
    """
    ispin, total_dos_np, Efermi, energy, pdos_raw_data = load_doscar_raw_data(path=DOSCAR_path)

    if absolute:
        energy = energy + Efermi

    def plot_total(energy0, total_dos, label=None):
        plt.plot(energy0, total_dos, color='black', linewidth=0.5, alpha=0.5, label=label)



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


    elements_label, elements_array = read_poscar.read_element(POSCAR_path)

    for num, pdos in enumerate(pdos_list):
        for index1, atom_range in enumerate(atom_ranges):
            #print('this is index 1:  {}'.format(index1))
            pdos_slice = pdos.get_slice(start=atom_range[0], end=atom_range[1])
            drawing = Drawing(pdos_slice, include_orbitals=include_orbitals)
            #atom_label = "atom{}: {}".format(index1 + 1, atom_range)pw
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
                    linewidth=0.5,
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
                    linewidth=0.5,
                    label=resolve_label if (index2 == 0 and num == 1) else None
                )

    plt.xlim(xlim1, xlim2)
    plt.ylim(ylim1, ylim2)
    plt.xlabel(r"$E - E_{\mathrm{F}}$ (eV)", fontsize=16)
    plt.ylabel('PDOS (arb. unit)', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    if absolute:
        plt.axvline(x=Efermi, color='k', linestyle='--')
    else:
        plt.axvline(x=0, color='k', linestyle='--')

    lgd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True, ncol=8)



    if not nosize:
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(size_figure[0], size_figure[1], forward=True)

    if not notsave:
        plt.savefig('PDOS.png', bbox_extra_artists=[lgd], bbox_inches='tight')

    if pdf:
        plt.savefig('PDOS.pdf', bbox_extra_artists=[lgd], bbox_inches='tight')


    if not notshow:
        plt.show()