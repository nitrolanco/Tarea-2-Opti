import pulp
import matplotlib.pyplot as plt
import random
import math


def atsp_gg(instance):
    problema = pulp.LpProblem("Problema_de_Rutas_Mínimas", pulp.LpMinimize)

    n = len(instance)
    V = range(n)  # Donde 'n' es el número de nodos
    A = [(i, j) for i in V for j in V if i != j]
    G = [(i, j) for i in range(1, n) for j in V if i != j]
    x = pulp.LpVariable.dicts("x", A, 0, 1, pulp.LpBinary)
    # u = pulp.LpVariable.dicts("u", V, 0, n, pulp.LpInteger )
    # Función objetivo
    problema += pulp.lpSum(instance[i][j] * x[(i, j)] for (i, j) in A)
    g = pulp.LpVariable.dicts("g", G, 0, n - 1, pulp.LpInteger)
    # Restricciones
    for i in V:
        problema += pulp.lpSum(x[(i, j)] for j in V if i != j) == 1

    for j in V:
        problema += pulp.lpSum(x[(i, j)] for i in V if i != j) == 1

    for i in range(1, n):
        problema += (
            pulp.lpSum(g[(i, j)] for j in V if i != j)
            - pulp.lpSum(g[(j, i)] for j in range(1, n) if i != j)
        ) == 1

    for i in range(1, n):
        for j in V:
            if i != j:
                problema += 0 <= g[(i, j)]
                problema += g[(i, j)] <= (n - 1) * x[(i, j)]

    problema.solve()

    # Imprimir la solución
    print("Status:", pulp.LpStatus[problema.status])
    for i, j in A:
        if x[(i, j)].varValue == 1:
            print(f"x({i},{j}) = 1")
    print("Optimal value =", pulp.value(problema.objective))
    return x


def get_instance(filename, quantity=10):
    path = "instances/"
    instance = [
        [float(j) for j in i.split(" ")]
        for i in open(path + filename, "r").read().split("\n")[7:-2]
    ]
    instance = random.sample(
        instance, quantity
    )  # Reduzco el tamaño por tiempos de computo

    return instance


def solve_instance_gg(instance):
    c = []
    for i in range(len(instance)):
        aux = []
        for j in range(len(instance)):
            pt1 = (instance[i][1], instance[i][2])
            pt2 = (instance[j][1], instance[j][2])
            aux.append(math.dist(pt1, pt2))
        c.append(aux)
    return atsp_gg(c)


def plot_instance(x, instance):
    A = [(i, j) for i in range(len(instance)) for j in range(len(instance)) if i != j]
    arcos_solucion = [(i, j) for i, j in A if x[(i, j)].varValue == 1]
    print(arcos_solucion)

    plt.figure(figsize=(7, 8))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Problema TSP")
    x_coord = [i[1] for i in instance]
    y_coord = [i[2] for i in instance]
    plt.scatter(x=x_coord, y=y_coord, color="blue", zorder=1)

    for i, j in arcos_solucion:
        plt.plot(
            [x_coord[i], x_coord[j]], [y_coord[i], y_coord[j]], color="blue", zorder=1
        )

    plt.show()
