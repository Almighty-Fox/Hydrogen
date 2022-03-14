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

    for jj in range(num_kan):
        for node in nodes[jj]:  # заоплняем начальные массивы концентрации, температуры
            concentration[jj].append(node.ci)
            temperature[jj].append(node.ti)

    coordinate = []  # вводим массив для координат, задаем один раз до цикла по времени
    for node in nodes[0]:  # заполняем постоянный массив координат
        coordinate.append(node.ri)

    # заполняем одним значением поток до процесса диффузии
    for jj in range(num_kan):
        flow = -nodes[jj][MaxNode - 1].di * (nodes[jj][MaxNode - 1].ci - nodes[jj][MaxNode - 2].ci) / (nodes[jj][MaxNode - 1].ri - nodes[jj][MaxNode - 2].ri)
        Flow[jj].append(flow)

    # ---------- задание графиков -------------------------
    fig, axs = plt.subplots(3)
    plt.subplots_adjust(wspace=0.6, hspace=0.6)
    fig.suptitle('ГРАФИКИ')
    # -----------------------------------

    t = Dt  # первый момент времени равен одному шагу по времени
    # вынесли цикл по времени над разделениями по потокам. То есть деление по потокам происходит каждый момент времени.
    while t <= time0:
        with futures.ThreadPoolExecutor(max_workers=num_kan) as executor:  # начинаем создавать потоки
            for jj in range(num_kan):
                future = executor.submit(main_body_fun, D0[jj], LLL[jj], UUU[jj], kkk, To, VL, VT1, K1, DT1, MaxNode, Dt, time0, C0[jj], nodes[jj], jj, t)  # запускаем потоки

        sum_concentration = np.zeros(MaxNode)  # создаем массив для суммарной концентрации
        for ii in range(num_kan):
            sum_concentration += np.array(concentration[ii])

        time_plot.append(t)

        # -----------------------------------
        axs[0].plot(coordinate, sum_concentration, 'r', linewidth=1)
        axs[1].plot(time_plot[1:], sum(np.array(Flow))[1:], 'r', linewidth=1)
        axs[2].plot(coordinate, temperature[0][:], 'r', linewidth=1)
        axs[0].set_title("Time = " + str(t))
        if sum(np.array(Flow))[-1] < sum(np.array(Flow))[-2]:
            axs[1].set_title('Поток ⟱')
        else:
            axs[1].set_title('Поток ⟰')
        axs[2].set_title('Temperature')
        plt.pause(0.0001)
        axs[0].clear()
        axs[1].clear()
        axs[2].clear()
        # ---------------------------

        t += Dt
