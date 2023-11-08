import sys
import atsp_gg as gg


def main():
    file_name = sys.argv[1]

    if sys.argv[2] != None:
        instance = gg.get_instance(file_name, int(sys.argv[2]))
    else:
        gg.get_instance(file_name)

    # x es el conjunto de arcos que forman la solución óptima

    x = gg.solve_instance_gg(instance)
    gg.plot_instance(x, instance)


main()
