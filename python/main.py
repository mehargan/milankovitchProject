import matplotlib as plt
import sys
import numpy as np

from milankovitch import Milankovitch
from lookUpMatrix import LookUp

def main():

    # plt.close('all')
    # sys.path.append('/Users/damaya/Desktop/matlab_scripts/')
    # sys.path.append('/Users/damaya/Desktop/matlab_scripts/snctools')

    # intv = np.arange(1,5000+2,1)

    # #Example 1: Summer solstice insolation at 65 N')
    # Fsw = Milankovitch.daily_insolation(np.arange(0,1000+2),65,90,2)
    # plt.plot(np.arange(0,1000+2,1),Fsw)
    # plt.ylabel('Insolation @ 65˚N on the Summer Solstice', fontweight='bold')
    # plt.xlabel('Thousands of years before present', fontweight='bold')
    # plt.show()
    # ##
    # #Example 2: Difference between June 20 (calendar day) and summer solstice insolation at 65 N
    # Fsw = Milankovitch.daily_insolation(np.arange(0,100+2), 65, 90, 2)
    # plt.ylabel('Insolation @ 65˚N on the Summer Solstice', fontweight='bold')
    # plt.xlabel('Thousands of years before present', fontweight='bold')
    # plt.plot(np.arange(0,100+2,1), Fsw)
    # plt.show()

    # LookUp.lookUpMatrix("matrix.txt",0.017644,23.573,84.26)
    LookUp.miniMatrix("matrix.txt", 0.000, 0.100, -150, -100, 22, 80.00, 100.00)

if __name__ == "__main__":
    main()
