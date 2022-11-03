import numpy as np
import matplotlib.pyplot as plt
import sys
import datetime as date
import scipy as scipy
import json

def mag_func(s):
    tok = []
    for t in s.strip('[]').split(';'):
        tok.append('[' + ','.join(t.strip().split(' ')) + ']')
    b = eval('[' + ','.join(tok) + ']')
    return np.array(b)

class LookUp:

    def readMatrix(matrix):
        with open('matrix.txt') as f:
            contents = f.read()
        m = mag_func(contents)
        return m
    
    def writeMatrix(dictionary):
        with open("miniMatrix.json", "w") as outfile:
            json.dump(dictionary, outfile)

    def lookUpMatrix( matrix, ecc=None, obliquity=None, precession=None):
        m = LookUp.readMatrix(matrix)
        eccTable = m[:,1]
        obliqTable = m[:,3]
        omegaTable = m[:,2]
        year = m[:,0]
        for e,o,p,y in zip(eccTable,obliqTable,omegaTable,year):
            if (ecc == e) and (obliquity == o) and (precession == p):
                print("year: ", int(y))

    def miniMatrix( matrix, minEcc, maxEcc, minYear, maxYear, minObl):
        m = LookUp.readMatrix(matrix)
        newMatrix = []
        eccTable = m[:,1]
        obliqTable = m[:,3]
        year = m[:,0]
        for e,o,y in zip(eccTable, obliqTable, year):
            if ((minEcc <= e) & (maxEcc >= e)) and ((minYear <= y) & (maxYear >= y)) \
            and (minObl <= o):
                temp = dict({"Ecc": e, "Obl": o, "Year": y})
                newMatrix.append(temp)
        LookUp.writeMatrix(newMatrix)
        

def main():
    #LookUp.lookUpMatrix("matrix.txt",0.017644,23.573,84.26)
    LookUp.miniMatrix("matrix.txt", 0.000, 0.100, -150, -100, 22)

if __name__ == "__main__":
    main()
