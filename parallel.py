from concurrent import futures
from main_body_parallel import *
import numpy as np
from nodes_class import ClassOFNodes
from global_var import *
from matplotlib import pyplot as plt


if __name__ == "__main__":
    global concentration, Flow, time_plot, temperature, Time_pik_1, Flow_pik_1

    nodes = [[ClassOFNodes(i, Rad, MaxNode) for i in range(MaxNode)] for jj in range(num_kan)]  # вводим массив объектов класса узлов

    for jj in range(num_kan):
        for node in nodes[jj]:  # назначаем начальную концентрацию, коэффициент диффузии и Т
                                # заоплняем начальные массивы концентрации, температуры
            node.determination_co(Rl[jj], width_l[jj], C1[jj], C2[jj], width_r[jj])
            node.determination_ti(To)
            node.determination_di(D0[jj], UUU[jj], kkk)
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
    fig, axs = plt.subplots(3, 1, gridspec_kw={'height_ratios': [2, 2, 1]})
    plt.subplots_adjust(wspace=0.6, hspace=0.6)
    fig.suptitle('ГРАФИКИ')
    # axs[1].legend("Sum", "1", "2", "3", "4")
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
        if t > Dt:
            if (sum(np.array(Flow))[-2] > sum(np.array(Flow))[-1]) and (sum(np.array(Flow))[-2] > sum(np.array(Flow))[-3]):
                Time_pik_1 = t - Dt
                Flow_pik_1 = sum(np.array(Flow))[-2]
                print("Время пика {0:.2f}, поток {1:0.4g}".format(Time_pik_1, Flow_pik_1))
        # -----------------------------------
        axs[0].plot(coordinate, sum_concentration, 'r--', linewidth=2)
        for ii in range(num_kan):  # строим поток каждого канала отдельно
            axs[0].plot(coordinate, concentration[ii], linewidth=1)

        axs[1].plot(time_plot[0:], sum(np.array(Flow))[0:], 'g--', linewidth=2)  # строим суммарный поток
        for ii in range(num_kan):  # строим поток каждого канала отдельно
            axs[1].plot(time_plot[0:], Flow[ii][0:], linewidth=1)

        axs[2].plot(coordinate, temperature[0][:], 'g', linewidth=1)
        # axs[0].set_title("Time = " + str(t))
        axs[0].set_title("Распределение концентрации")
        fig.suptitle("Time = {0} c = {1:.2f} мин".format(t, t/60))
        if sum(np.array(Flow))[-1] < sum(np.array(Flow))[-2]:
            axs[1].set_title('Поток ⟱ ' + "Время пика {0:.2f}, поток {1:0.4g}".format(Time_pik_1, Flow_pik_1))
        else:
            axs[1].set_title('Поток ⟰ ' + "Время пика {0:.2f}, поток {1:0.4g}".format(Time_pik_1, Flow_pik_1))
        axs[2].set_title('Temperature {0:.2f}'.format(temperature[0][-1]))

        axs[0].legend(["Sum", "1", "2", "3", "4"])
        axs[1].legend(["Sum", "1", "2", "3", "4"])
        plt.pause(0.0001)

        axs[0].clear()
        axs[1].clear()
        axs[2].clear()
        # ---------------------------

        t += Dt

    out = input()
