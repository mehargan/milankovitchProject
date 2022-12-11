import numpy as np
import matplotlib.pyplot as plt
import math

MAX_KYEARS = 151

class MilankovitchTable:
    def __init__(self) -> None:
        self.year_l  = np.empty(MAX_KYEARS)
        self.eccen_l = np.empty(MAX_KYEARS)
        self.omega_l = np.empty(MAX_KYEARS)
        self.obliq_l = np.empty(MAX_KYEARS)
        self.temp_l  = np.empty(MAX_KYEARS)
        self.insol_l = np.empty(MAX_KYEARS)

        self.m_params = {}

    def _mag_func(self, contents):
        tok = []
        for t in contents.strip('[]').split(';'):
            tok.append('[' + ','.join(t.strip().split(' ')) + ']')
        b = eval('[' + ','.join(tok) + ']')
        return np.array(b)

    def _normalize_insol(self, insol):
        range = np.max(self.insol_l) - np.min(self.insol_l)

        return (insol - np.min(self.insol_l)) / range

    def readMatrix(self):
        year, ecc, omega, obliq, _1, insol, _2, _3, _4 = np.loadtxt('./data/mtable.txt', unpack=True, skiprows=1)

        # m = self._mag_func(contents)
        self.year_l = np.array(year[:MAX_KYEARS])
        self.eccen_l = np.array(ecc[:MAX_KYEARS])
        self.omega_l = np.array(omega[:MAX_KYEARS])
        self.obliq_l = np.array(obliq[:MAX_KYEARS])
        self.insol_l = np.array(insol[:MAX_KYEARS])

    def readVostok(self):
        _depth, year, _deut, temp = np.loadtxt('./data/vostok.txt', unpack=True)
        self.temp_l[0] = 0.0
        
        mil = 1

        _sum = 0.0
        _num = 0
        for y, t in zip(year, temp):
            if y < mil * 1000:
                _sum += t
                _num += 1
            else :
                avg_temp = _sum / _num
                self.temp_l[mil] = avg_temp

                mil += 1
                _sum = 0.0
                _num = 0

                if mil == MAX_KYEARS: break

    def lookUp(self, omega, ecc):
        ind = np.where(np.isclose(self.omega_l, omega, atol=7.0) \
                        # & np.isclose(np.floor(self.obliq_l), 22.0) \
                        # & np.isclose(self.eccen_l, ecc, atol=0.002) \
                    )

        minEcc = (ecc < 0.02)

        if minEcc:
            i = self.eccen_l[ind].argmin()
        else :
            i = self.eccen_l[ind].argmax()

        mcycles = {}
        mcycles["year"] = int(ind[0][i])
        mcycles["omega"] = float(self.omega_l[ind[0][i]])
        mcycles["eccen"] = float(self.eccen_l[ind[0][i]])
        mcycles["obliq"] = float(self.obliq_l[ind[0][i]])
        mcycles["insol"] = float(self._normalize_insol(self.insol_l[ind[0][i]]))

        self.m_params = mcycles
        return mcycles

    # def daily_insolation(self, lat, day):


if __name__ == "__main__":
    table = MilankovitchTable()

    table.readMatrix()
    table.readVostok()

    for i in range(0, 360):
        mcycles_min = table.lookUp(i, True)
        mcycles_max = table.lookUp(i, False)
        print(f'Input: {i}, m-params-min: {mcycles_min}, m-params-max: {mcycles_max}')