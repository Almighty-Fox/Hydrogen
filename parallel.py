from concurrent import futures
from main_body_parallel import *
import numpy as np
from nodes_class import ClassOFNodes


if __name__ == "__main__":

    # ---------определяем параметры для диффузии и теплопроводности----------
    D0 = [8e-6, 8e-5]  # 8e-6 m^2/s ---------- коэф диффузии
    LLL = [3.352e-6, 2e-6]  # коэф температуропроводности нержавеющей стали
    UUU = [0.1, 0.3]  # eV ------- энергия связи
    kkk = 8.62e-5  # eV/K ------ коэф Больцмана
    To = 20 + 273  # 300  # K --------- начальная температура всего образца
    vel = 0.00  # скорость прогрева

    # ---------определяем параметры геометрии оброазца----------
    Rad = 2.2e-3 / 2  # m # mm r = 3e-3
    h = 0.6  # высота образца
    MaxNode = 10 + 1  # количесвто узлов
    DR = Rad / MaxNode
    Rl = Rad * 0.99
    width_l = 0.005 * Rad
    width_r = 0.005 * Rad

    # ---------определяем параметры времени----------
    time0 = 300  # s
    Dt = 10  # -------------------------------------------------------------------------------
    Time_pik_1 = 0
    Flow_pik_1 = 0

    # ---------определяем параметры концентрации----------
    C0 = [0, 0]  # Моль / м^3 # концентрация вне образца
    # C1 = 300  # 962.1169  # Моль / м^3 # концентрация внутри образца
    C1 = [160, 160]
    # C2 = 6000  # 962.1169  # Моль / м^3 # концентрация погран слоя
    C2 = [6000, 6000]

    # ---------параметры ловушек-----------
    VL = 4.9e-6  # 4.9e-6  # m^3/mol
    VT1 = 6e-5  # 6e-5  # m^3/mol
    # VT1 = 6e-10  # 6e-5  # m^3/mol
    K1 = 1.6e-5  # 2.0965e-16  # 1.6e-5  # skal
    DT1 = 1e-13
    # DT1 = 0
    # -----------------------------------

    num_kan = 2
    nodes = [[ClassOFNodes(i, Rad, MaxNode) for i in range(MaxNode)] for jj in range(num_kan)]  # вводим массив объектов класса узлов

    for jj in range(num_kan):
        for node in nodes[jj]:  # назначаем начальную концентрацию, коэффициент диффузии и Т
            node.determination_co(Rl, width_l, C1[jj], C2[jj], width_r)
            node.determination_ti(To)
            node.determination_di(D0[jj], UUU[jj], kkk)

    # concentration = []  # вводим массив для концентрации, будет обновляться каждый момент времени
    # concentration = np.zeros((num_kan, MaxNode))
    concentration = [[] for i in range(num_kan)]
    coordinate = []  # вводим массив для координат, задаем один раз до цикла по времени
    # temperature = []  # вводим массив для температуры, будет обновляться каждый момент времени
    # temperature = np.zeros((num_kan, MaxNode))
    temperature = [[] for i in range(num_kan)]

    # Flow = []  # вводим массив для потока, будет дополняться каждый момент времени
    Flow = [[] for i in range(num_kan)]
    # time_plot = [0]  # вводим массив для времени, будет дополняться каждый момент времени
    time_plot = [[0] for i in range(num_kan)]

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

        print("\nЗашел в потоки")

        for jj in range(num_kan):
            print("\nЦикл по потоку ", jj)
            future = executor.submit(main_body_fun, D0[jj], LLL[jj], UUU[jj], kkk, To, VL, VT1, K1, DT1, MaxNode, Dt, time0, C0[jj], nodes[jj], jj)
