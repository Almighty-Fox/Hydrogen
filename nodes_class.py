import math


class ClassOFNodes:
    """create class of nodes"""

    def __init__(self, i, rad, maxnode):
        """initiate"""
        self.ri = rad / (maxnode - 1) * i
        self.ci = 0
        self.di = 0
        self.ti = 0
        self.kai = 0
        self.kbi = 0
        self.kci = 0
        self.kfi = 0
        self.vi = 0
        self.si = 0
        self.vol1 = 0
        self.vol2 = 0
        self.alpha = 0
        self.betta = 0
        self.sss = 0
        self.CL = 0

    def determination_co(self, Rl, width_l, C1, C2, width_r):
        """sffeferfeferfe"""
        if self.ri < (Rl - width_l):
            self.ci = C1
        elif self.ri < Rl:
            self.ci = (C2-C1)/width_l * (self.ri - (Rl - width_l)) + C1
        elif self.ri < (Rl + width_r):
            self.ci = -C2/width_r * (self.ri - (Rl + width_r))
        else:
            self.ci = 0

    def determination_ti(self, TTT):
        """firesafe"""
        self.ti = TTT

    def determination_di(self, do, UUU, kkk):
        """sffeferfeferfe"""
        # self.di = do * math.exp((-UUU / (kkk * self.ti)))
        self.di = 1e-9  # m^2/s

    def determination_cl(self, CLL):
        """sffeferfeferfe"""
        self.CL = CLL

    def determination_di_lovushki(self, do, UUU, kkk, VL, VT1, K1, DT1):
        """sffeferfeferfe"""
        # dl = do * math.exp((-UUU / (kkk * self.ti)))
        dl = 1e-9  # m^2/s
        slag = (VL / VT1 * K1 / (K1 + VL * self.CL * (1 - K1))**2)
        self.di = (dl + DT1 * slag) * (1 + slag)**(-1)

    def determination_abcf_zero(self):
        self.kai = 0
        self.kbi = 0
        self.kci = 0
        self.kfi = 0

    def determination_abcf(self, node_sled, drr, dt, vol1, vol2, sss):
        self.kbi = sss * self.di / drr
        self.kci += self.kbi + vol1 / dt
        self.kfi += self.ci * vol1 / dt
        node_sled.kai = sss * self.di / drr
        node_sled.kci += node_sled.kai + vol2 / dt
        node_sled.kfi += node_sled.ci * vol2 / dt

    def determination_abcf_tempr(self, node_sled, drr, dt, vol1, vol2, sss, LLL):
        self.kbi = sss * LLL / drr
        self.kci += self.kbi + vol1 / dt
        self.kfi += self.ti * vol1 / dt
        node_sled.kai = sss * LLL / drr
        node_sled.kci += node_sled.kai + vol2 / dt
        node_sled.kfi += node_sled.ti * vol2 / dt

    def determination_abcf_gu(self, C0):
        self.kai = 0
        self.kbi = 0
        self.kci = 1
        self.kfi = C0
