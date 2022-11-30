from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET  # для чтения файлов xml
import numpy as np
import pandas as pd
import seaborn as sns


def def_read_xml(name_xml):  # функция чтения значений из xml
    tree = ET.parse(name_xml)
    root = tree.getroot()

    XValue = []
    YValue = []

    for point in root.findall('Datas/Point'):
        XValue.append(point.get('XValue'))
        YValue.append(point.get('YValue'))

    return XValue, YValue


def change_point(x, y):  # меняем запятые на точки
    for ii in range(len(x)):
        x[ii] = float(x[ii])
        y[ii] = float(y[ii].replace(',', '.'))

    return x, y


def grafik(x, y):
    plt.plot(x, y, 'r', linewidth=1)
    # plt.show()


def grafik_average(x, y):  # рисуем каждую 100 точку
    Interval = 100
    ii = 0
    x_average = []
    y_average = []
    while ii < len(x):
        x_average.append(x[ii])
        y_average.append(y[ii])

        ii += Interval

    plt.plot(x_average, y_average, 'g', linewidth=1)
    # plt.show()


def grafik_average_2(x, y):  # осредняем каждые 100 точек
    # print(len(x))
    Interval = 10
    N = len(x) // Interval  # целая часть от деления
    M = len(x) % Interval  # дробная часть от деления
    x_average = []
    y_average = []

    for ii in range(N):
        sum_y = sum(y[(ii * Interval):((ii + 1) * Interval)])
        y_av = sum_y / Interval
        y_average.append(y_av)

        x_average.append(x[(ii * Interval + Interval // 2)])

    sum_y = sum(y[(N * Interval):])
    if M != 0:
        y_av = sum_y / M
    else:
        y_av = y_average[-1]
    y_average.append(y_av)
    x_average.append(x[-1])
    # print(len(x_average), len(y_average))

    plt.plot(x_average, y_average, 'b', linewidth=1)
    # plt.show()

    return x_average, y_average


if __name__ == "__main__":

    name_file = r'F:\Evgenii\Hydrogen_\ДЕванатан_x70\деванотан_часть1_№6_исх.xml'

    [x, y] = def_read_xml(name_file)  # заполняем массивы для графика
    [x, y] = change_point(x, y)  # меняем запятые на точки

    plt.figure(1)
    grafik(x, y)  # строим исходный график
    # plt.title(sample[ii])
    plt.title("Экспериментальная десорбционная кривая")
    plt.xlabel("Time")
    plt.ylabel("Flow")
    plt.grid()
    # ----- строим коридоры -------
    num_ex = 7
    for i in np.linspace(min(x), max(x), num_ex):
        plt.plot([i, i], [min(y), max(y)], '--k', linewidth=1)
    # -----------------------------
    # plt.show()

    # -------------- выделяем один пик --------
    xx_begin = 6.32e3
    xx_end = 7.15e3
    id_begin = 0
    id_end = max(x)
    for ID, i in enumerate(x):
        if i > xx_begin:
            id_begin = ID
            break
    for ID, i in enumerate(x[id_begin:]):
        if i > xx_end:
            id_end = ID + id_begin
            break
    print("ID begin = {}".format(id_begin))
    print("ID end = {}".format(id_end))
    df = pd.DataFrame(dict(x=x[id_begin:id_end], y=y[id_begin:id_end]))
    # -----------------------------------------
    # ------ рисуем выделенный пик -------
    plt.figure()
    sns.lineplot(x=df.x, y=df.y)
    plt.title("Экспериментальная десорбционная кривая")
    plt.xlabel("Time")
    plt.ylabel("Flow")
    plt.grid()
    # ------ рисуем сглаженный выделенный пик -------
    plt.figure()
    df2 = df.rolling(window=10).mean()
    sns.lineplot(x=df2.x, y=df2.y)
    plt.title("Экспериментальная десорбционная кривая")
    plt.xlabel("Time")
    plt.ylabel("Flow")
    plt.grid()

    plt.show()

    """
    division_points = [[3967, 6547], [7299, 9877], [10292, 12365], [13148, 14995], [15447, 18678]]
    sample = ["7 мм", "6 мм", "5 мм", "4 мм", "8 мм"]

    try:
        [x, y] = def_read_xml(name_file)  # заполняем массивы для графика
        [x, y] = change_point(x, y)  # меняем запятые на точки

        x_inter, y_inter = [], []

        for ii in range(len(division_points)):
            x_inter.append(range(len(x[division_points[ii][0]:division_points[ii][1]])))  # сдвигаем по иксу на 0
            y_inter.append(y[division_points[ii][0]:division_points[ii][1]])

        # for ii in range(len(division_points)):
        for ii in range(1):
            plt.figure(ii+1)
            grafik(x_inter[ii], y_inter[ii])  # строим исходный график
            # plt.title(sample[ii])
            plt.title("Экспериментальная десорбционная кривая")
            plt.xlabel("Time")
            plt.ylabel("Flow")
            plt.grid()

            grafik_average_2(x_inter[ii], y_inter[ii])
            # plt.figure(ii+10)
            # grafik_average_2(x_inter[ii], y_inter[ii])
            # plt.title(sample[ii])

        plt.savefig('experimental_7.png')
        plt.savefig('experimental_7_2.png', dpi=1000)
        plt.show()

    except:
        print('все плохо, не могу открыть ', name_file)
        
    """""
