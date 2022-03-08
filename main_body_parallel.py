from math import *
from matplotlib import pyplot as plt
from nodes_class import ClassOFNodes
from progonka import neyavnaya_progonka
from progonka_tempr import neyavnaya_progonka_tempr
from eq_for_lovushek import function_for_lovushek
from scipy.optimize import fsolve
import numpy


def main_body_fun(D0, LLL, UUU, kkk, To, VL, VT1, K1, DT1, MaxNode, Dt, time0, C0, nodes_index, index):
    global concentration, Flow, time_plot
    print("\nЗашел в поток ", index)
    # plt.style.use('seaborn-pastel')

    # ----------------------------------
    # fig, axs = plt.subplots(3)
    # # fig_2, axs_2 = plt.subplots(3)
    # plt.subplots_adjust(wspace=0.6, hspace=0.9)
    # fig.suptitle('ГРАФИКИ')
    # axs[0].plot(coordinate, concentration, 'r', linewidth=1)
    # axs[1].plot(time_plot, Flow, 'g', linewidth=1)
    # axs[2].plot(coordinate, temperature, 'b', linewidth=1)
    # axs[0].set_title('Дисперсионная кривая')
    # axs[1].set_title('Поток')
    # axs[2].set_title('Температура')
    # plt.pause(2)
    # axs[0].clear()
    # axs[1].clear()
    # axs[2].clear()
    # # plt.clf()
    # -----------------------------------

    t = Dt  # первый момент времени равен одному шагу по времени

    while t <= time0:
        print("1. Time in thread ", index, " = ", t)

        # TTT = To + vel * t  # опрелеяем температуру воздуха в данный момент времени
        TTT = 750 + 273

        # --------------решаем уравнение теплопроводности------------
        for node in nodes_index:
            node.determination_abcf_zero()  # обнуляем коэффициенты

        print("2. Time in thread ", index, " = ", t)

        for ID, node in enumerate(nodes_index[0:(MaxNode - 1)], start=0):  # находим коэф a,b,c,d для всех узлов
            # РАБОТАЕМ В ЦИЛИНДРИЧЕСКОЙ СК
            r1 = node.ri  # координата текущего узла
            r2 = nodes_index[ID + 1].ri  # координата следующего узла

            dr = r2 - r1
            rc = 0.5 * (r1 + r2)
            vol1 = pi * (rc * rc - r1 * r1)
            vol2 = pi * (r2 * r2 - rc * rc)
            sss = 2 * pi * rc

            node.determination_abcf_tempr(nodes_index[ID + 1], dr, Dt, vol1, vol2, sss,
                                          LLL)  # находим коэф a,b,c,d для всех узлов

        nodes_index[MaxNode - 1].determination_abcf_gu(TTT)  # определяем ГУ для коэф a,b,c,d

        # ------------------прогонка неявного метода---------------------------------
        nodes_index = neyavnaya_progonka_tempr(nodes_index, MaxNode)
        # ------------------конец прогонки---------------------------------
        # -----------конец решения уравнения теплопроводности-----------------------

        # раньше так определяли коэф диффузии, он зависил только от температуры
        # (и постоянных: коэф диф, эн связи, коэф Больцмана)

        # for node in nodes:
        #     node.determination_di(D0, UUU, kkk)  # определяем коэф диффузии в данный момент времени в данном узле

        print("3. Time in thread ", index, " = ", t)

        # теперь считаем коэф диффузии с учетом ловушек
        for node in nodes_index:
            CL_ = fsolve(function_for_lovushek, numpy.array([0.2]), args=(VL, VT1, K1, node.ci))
            node.determination_cl(CL_[0])
            node.determination_di_lovushki(D0, UUU, kkk, VL, VT1, K1, DT1)

        # --------------решаем уравнение диффузии------------
        for node in nodes_index:
            node.determination_abcf_zero()  # обнуляем коэффициенты

        for ID, node in enumerate(nodes_index[0:(MaxNode - 1)], start=0):  # находим коэф a,b,c,d для всех узлов
            # РАБОТАЕМ В ЦИЛИНДРИЧЕСКОЙ СК
            r1 = node.ri  # координата текущего узла
            r2 = nodes_index[ID + 1].ri  # координата следующего узла

            dr = r2 - r1
            rc = 0.5 * (r1 + r2)
            vol1 = pi * (rc * rc - r1 * r1)
            vol2 = pi * (r2 * r2 - rc * rc)
            sss = 2 * pi * rc

            node.determination_abcf(nodes_index[ID + 1], dr, Dt, vol1, vol2, sss)  # находим коэф a,b,c,d для всех узлов

        nodes_index[MaxNode - 1].determination_abcf_gu(C0)  # определяем ГУ для коэф a,b,c,d

        print("4. Time in thread ", index, " = ", t)

        # ------------------прогонка неявного метода---------------------------------
        nodes_index = neyavnaya_progonka(nodes_index, MaxNode)
        # ------------------конец прогонки---------------------------------
        # -----------конец решения уравнения диффузии-----------------------
        print("5. Time in thread ", index, " = ", t)
        # нашли концентрацию во всех узлах в следующий момент времени
        print("6. Time in thread ", index, " = ", t)
        print(concentration)
        concentration[index] = []
        print("7. Time in thread ", index, " = ", t)
        temperature = []
        print("8. Time in thread ", index, " = ", t)
        for node in nodes_index:
            # concentration[index].append(node.ci)
            temperature.append(node.ti)

        print("9. Time in thread ", index, " = ", t)

        # flow = -nodes_index[MaxNode - 1].di * (nodes_index[MaxNode - 1].ci - nodes_index[MaxNode - 2].ci) / (
        #         nodes_index[MaxNode - 1].ri - nodes_index[MaxNode - 2].ri)
        # # print(flow)
        # Flow[index].append(flow)
        # time_plot[index].append(t)

        print("11. Time in thread ", index, " = ", t)

        # if t > Dt:
        #     if (Flow[-2] > Flow[-1]) and (Flow[-2] > Flow[-3]):
        #         Time_pik_1 = t - Dt
        #         Flow_pik_1 = Flow[-2]

        # ----------------------------------
        # axs[0].set_title('Дисперсионная кривая')
        # axs[1].set_title(
        #     'Поток.\n Время пика = ' + str(Time_pik_1) + '. Поток во время пика = ' + '%s' % float('%.3g' % Flow_pik_1))
        # axs[2].set_title('Температура на краю = ' + str(TTT) + '\n')
        # fig.suptitle('Время = ' + str(t)
        #              + ' c = ' + str('%.2f' % (t / 60)) + ' мин = ' + str('%.2f' % (t / 60 / 60)) + ' ч')
        # axs[0].plot(coordinate, concentration, 'r', linewidth=1)
        # axs[1].plot(time_plot, Flow, 'g', linewidth=1)
        # axs[2].plot(coordinate, temperature, 'b', linewidth=1)
        # # axs[2].axis([0, coordinate[-1], 0, temperature[-1]*1.2])  # устанавливаем диапозон осей
        # plt.pause(0.01)
        # axs[0].clear()
        # axs[1].clear()
        # axs[2].clear()

        print("Канал ", index, " время ", t)
        t += Dt
        # --------------------------------

    # plt.pause(20)


def main_body_fun_test(D0, LLL, UUU, kkk, To, VL, VT1, K1, DT1, MaxNode, Dt, time0, C0, nodes_index, index):
    t = Dt
    while t <= time0:
        print("Канал ", index, " время ", t)
        t += Dt