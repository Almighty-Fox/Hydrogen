from math import *
from matplotlib import pyplot as plt
from nodes_class import ClassOFNodes
from progonka import neyavnaya_progonka
from progonka_tempr import neyavnaya_progonka_tempr
from eq_for_lovushek import function_for_lovushek
from scipy.optimize import fsolve
import numpy


def main_body_fun(D0_list, L_list, U_list, k_list, T0, VL_list, VT1_list, K1_list, DT1_list):
    # plt.style.use('seaborn-pastel')



    nodes = [ClassOFNodes(i, Rad, MaxNode) for i in range(MaxNode)]  # вводим массив объектов класса узлов

    for ID, node in enumerate(nodes, start=0):  # назначаем начальную концентрацию, коэффициент диффузии и Т
        node.determination_co(Rl, width_l, C1, C2, width_r)
        node.determination_ti(To)
        node.determination_di(D0, UUU, kkk)

    concentration = []  # вводим массив для концентрации, будет обновляться каждый момент времени
    coordinate = []  # вводим массив для координат, задаем один раз до цикла по времени
    temperature = []  # вводим массив для температуры, будет обновляться каждый момент времени
    Flow = []  # вводим массив для потока, будет дополняться каждый момент времени
    time_plot = [0]  # вводим массив для времени, будет дополняться каждый момент времени

    for node in nodes:  # заоплняем начальные массивы концентрации, температуры и постоянный массив координат
        coordinate.append(node.ri)
        concentration.append(node.ci)
        temperature.append(node.ti)

    # заполняем одним значением поток до процесса диффузии
    flow = -nodes[MaxNode - 1].di * (nodes[MaxNode - 1].ci - nodes[MaxNode - 2].ci) / (nodes[MaxNode - 1].ri - nodes[MaxNode - 2].ri)
    Flow.append(flow)

    # ----------------------------------
    fig, axs = plt.subplots(3)
    # fig_2, axs_2 = plt.subplots(3)
    plt.subplots_adjust(wspace=0.6, hspace=0.9)
    fig.suptitle('ГРАФИКИ')
    axs[0].plot(coordinate, concentration, 'r', linewidth=1)
    axs[1].plot(time_plot, Flow, 'g', linewidth=1)
    axs[2].plot(coordinate, temperature, 'b', linewidth=1)
    axs[0].set_title('Дисперсионная кривая')
    axs[1].set_title('Поток')
    axs[2].set_title('Температура')
    plt.pause(2)
    axs[0].clear()
    axs[1].clear()
    axs[2].clear()
    # plt.clf()
    # -----------------------------------

    t = Dt  # первый момент времени равен одному шагу по времени

    while t <= time0:

        # TTT = To + vel * t  # опрелеяем температуру воздуха в данный момент времени
        TTT = 750 + 273

        # --------------решаем уравнение теплопроводности------------
        for node in nodes:
            node.determination_abcf_zero()  # обнуляем коэффициенты

        for ID, node in enumerate(nodes[0:(MaxNode - 1)], start=0):  # находим коэф a,b,c,d для всех узлов
            # РАБОТАЕМ В ЦИЛИНДРИЧЕСКОЙ СК
            r1 = node.ri  # координата текущего узла
            r2 = nodes[ID + 1].ri  # координата следующего узла

            dr = r2 - r1
            rc = 0.5 * (r1 + r2)
            vol1 = pi * (rc * rc - r1 * r1)
            vol2 = pi * (r2 * r2 - rc * rc)
            sss = 2 * pi * rc

            node.determination_abcf_tempr(nodes[ID + 1], dr, Dt, vol1, vol2, sss,
                                          LLL)  # находим коэф a,b,c,d для всех узлов

        nodes[MaxNode - 1].determination_abcf_gu(TTT)  # определяем ГУ для коэф a,b,c,d

        # ------------------прогонка неявного метода---------------------------------
        nodes = neyavnaya_progonka_tempr(nodes, MaxNode)
        # ------------------конец прогонки---------------------------------
        # -----------конец решения уравнения теплопроводности-----------------------

        # раньше так определяли коэф диффузии, он зависил только от температуры
        # (и постоянных: коэф диф, эн связи, коэф Больцмана)

        # for node in nodes:
        #     node.determination_di(D0, UUU, kkk)  # определяем коэф диффузии в данный момент времени в данном узле

        # теперь считаем коэф диффузии с учетом ловушек
        for node in nodes:
            CL_ = fsolve(function_for_lovushek, numpy.array([0.2]), args=(VL, VT1, K1, node.ci))
            node.determination_cl(CL_[0])
            node.determination_di_lovushki(D0, UUU, kkk, VL, VT1, K1, DT1)

        # --------------решаем уравнение диффузии------------
        for node in nodes:
            node.determination_abcf_zero()  # обнуляем коэффициенты

        for ID, node in enumerate(nodes[0:(MaxNode - 1)], start=0):  # находим коэф a,b,c,d для всех узлов
            # РАБОТАЕМ В ЦИЛИНДРИЧЕСКОЙ СК
            r1 = node.ri  # координата текущего узла
            r2 = nodes[ID + 1].ri  # координата следующего узла

            dr = r2 - r1
            rc = 0.5 * (r1 + r2)
            vol1 = pi * (rc * rc - r1 * r1)
            vol2 = pi * (r2 * r2 - rc * rc)
            sss = 2 * pi * rc

            node.determination_abcf(nodes[ID + 1], dr, Dt, vol1, vol2, sss)  # находим коэф a,b,c,d для всех узлов

        nodes[MaxNode - 1].determination_abcf_gu(C0)  # определяем ГУ для коэф a,b,c,d

        # ------------------прогонка неявного метода---------------------------------
        nodes = neyavnaya_progonka(nodes, MaxNode)
        # ------------------конец прогонки---------------------------------
        # -----------конец решения уравнения диффузии-----------------------

        # нашли концентрацию во всех узлах в следующий момент времени
        concentration = []
        temperature = []
        for node in nodes:
            concentration.append(node.ci)
            temperature.append(node.ti)

        flow = -nodes[MaxNode - 1].di * (nodes[MaxNode - 1].ci - nodes[MaxNode - 2].ci) / (
                nodes[MaxNode - 1].ri - nodes[MaxNode - 2].ri)
        # print(flow)
        Flow.append(flow)
        time_plot.append(t)

        if t > Dt:
            if (Flow[-2] > Flow[-1]) and (Flow[-2] > Flow[-3]):
                Time_pik_1 = t - Dt
                Flow_pik_1 = Flow[-2]

        # ----------------------------------
        axs[0].set_title('Дисперсионная кривая')
        axs[1].set_title(
            'Поток.\n Время пика = ' + str(Time_pik_1) + '. Поток во время пика = ' + '%s' % float('%.3g' % Flow_pik_1))
        axs[2].set_title('Температура на краю = ' + str(TTT) + '\n')
        fig.suptitle('Время = ' + str(t)
                     + ' c = ' + str('%.2f' % (t / 60)) + ' мин = ' + str('%.2f' % (t / 60 / 60)) + ' ч')
        axs[0].plot(coordinate, concentration, 'r', linewidth=1)
        axs[1].plot(time_plot, Flow, 'g', linewidth=1)
        axs[2].plot(coordinate, temperature, 'b', linewidth=1)
        # axs[2].axis([0, coordinate[-1], 0, temperature[-1]*1.2])  # устанавливаем диапозон осей
        plt.pause(0.01)
        axs[0].clear()
        axs[1].clear()
        axs[2].clear()

        t += Dt
        # --------------------------------

    plt.pause(20)
