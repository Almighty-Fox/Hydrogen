from concurrent import futures
from main_body_parallel import *
import numpy as np
from nodes_class import ClassOFNodes
from global_var import *


if __name__ == "__main__":
    global concentration, Flow, time_plot, temperature

    nodes = [[ClassOFNodes(i, Rad, MaxNode) for i in range(MaxNode)] for jj in range(num_kan)]  # вводим массив объектов класса узлов

    for jj in range(num_kan):
        for node in nodes[jj]:  # назначаем начальную концентрацию, коэффициент диффузии и Т
            node.determination_co(Rl, width_l, C1[jj], C2[jj], width_r)
            node.determination_ti(To)
            node.determination_di(D0[jj], UUU[jj], kkk)

    coordinate = []  # вводим массив для координат, задаем один раз до цикла по времени

    for jj in range(num_kan):
        for node in nodes[jj]:  # заоплняем начальные массивы концентрации, температуры и постоянный массив координат
            concentration[jj].append(node.ci)
            temperature[jj].append(node.ti)

    for node in nodes[0]:
        coordinate.append(node.ri)

    # заполняем одним значением поток до процесса диффузии
    for jj in range(num_kan):
        flow = -nodes[jj][MaxNode - 1].di * (nodes[jj][MaxNode - 1].ci - nodes[jj][MaxNode - 2].ci) / (nodes[jj][MaxNode - 1].ri - nodes[jj][MaxNode - 2].ri)
        Flow[jj].append(flow)

    with futures.ThreadPoolExecutor(max_workers=3) as executor:

        for jj in range(num_kan):
            future = executor.submit(main_body_fun, D0[jj], LLL[jj], UUU[jj], kkk, To, VL, VT1, K1, DT1, MaxNode, Dt, time0, C0[jj], nodes[jj], jj)

    sum_concentration = np.zeros(MaxNode)
    for ii in range(num_kan):
        sum_concentration += np.array(concentration[ii])
    plt.plot(coordinate, sum_concentration, 'r', linewidth=1)
    plt.show()
