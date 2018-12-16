import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import pandas.plotting._converter as pandacnv
pandacnv.register()

style.use('seaborn-whitegrid')


df = pd.read_csv('data/DAT_ASCII_EURUSD_M1_2015.csv', ';',
  parse_dates=True, index_col=0, names=['o', 'h', 'l', 'c', 'v'])

close = df.c[-20:].values.tolist()
spread = 0.00020
rstoploss = -0.001
rtakeprofit = 0.001
print(close)

oposs = []
cposs = []

class Pos():
    def __init__(self, op):
        self.top = None
        self.tcl = None
        self.op = None
        self.cl = None
        self.rpr = None
        self.open(op)

    def __repr__(self):
        return '(o: %s, c: %s, pr: %s)' % (self.op, self.cl, self.rpr)

    def open(self, op):
        self.op = op

    def checkClose(self, cl):
        rprofit = (cl - self.op) / self.op
        if rstoploss < rprofit < rtakeprofit:
            return False
        self.close(cl)
        return True

    def close(self, cl):
        rprofit = (cl - self.op) / self.op
        self.cl = cl
        self.rpr = rprofit
        oposs.remove(pos)
        cposs.append(pos)

for price in close:
    oposs.append(Pos(price))
    for pos in oposs:
        pos.checkClose(price - spread)
print(len(oposs))
print(len(cposs))


print(oposs)
print(cposs)

plt.plot(close)
plt.show()