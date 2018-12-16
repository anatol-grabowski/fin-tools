import numpy as np
import pandas as pd
import pyqtgraph as pg


def read_data():
    filename = '/home/tot/_tot/projects/data/EUR_USD_Week1.csv'
    df = pd.read_csv(filename,
                     names=['Tid', 'Dealable', 'Pair', 'time', 'bid', 'ask'],
                     index_col='time',
                     parse_dates=['time'],
                     header=0)
    del df['Tid']
    del df['Dealable']
    del df['Pair']
    del df['bid']
    return df


def resample_data(df):
    df = df.resample('1T').mean()  # should use ohlc
    return df


def calc_MAs(df, num_mas=5):
    mas = [str(2 ** (x + 1)) + 'T' for x in range(num_mas)]
    for ma in mas:
        df.loc[:, 'MA_' + ma] = df.rolling(ma).mean()


def calc_rMADs(df):
    for s in df:
        if not s.startswith('MA_'):
            continue
        ma = s.split('_')[1]
        df.loc[:, 'rMAD_' + ma] = 1 - df['MA_' + ma] / df['ask']


def calc_profits(df):
    rstoploss = -0.0006
    rtakeprofit = 0.0008
    rspread = 0.0004
    oposs = []
    df.loc[:, 'pos_opn'] = pd.Series(np.zeros(len(df)), index=df.index)
    df.loc[:, 'pos_clo'] = pd.Series(np.zeros(len(df)), index=df.index)
    df.loc[:, 'time_clo'] = pd.Series(df.index.copy(), index=df.index)
    df.loc[:, 'rporfit'] = pd.Series(df.index.copy(), index=df.index)
    for i in range(len(df)):
        time = df.index[i]
        ask = df['ask'].iloc[i]
        pos = (time, ask)
        oposs.append(pos)
        bid = ask * (1 - rspread)
        for j in reversed(range(len(oposs))):
            opos = oposs[j]
            rprofit = (bid - opos[1]) / opos[1]
            if rstoploss < rprofit < rtakeprofit:
                continue
            del oposs[j]
            df.loc[opos[0], 'pos_opn'] = opos[1]
            df.loc[opos[0], 'pos_clo'] = bid
            df.loc[opos[0], 'time_clo'] = time
            df.loc[opos[0], 'rprofit'] = rprofit


def plot_data(df):
    t = df.index.values.astype('int64')
    win = pg.GraphicsWindow(title='ppp')
    plt_price = win.addPlot(title='price + MAs', row=0, col=0)
    plt_price.plot(t, df['ask'], symbol='o')
    plt_rmads = win.addPlot(title='rMADs', row=1, col=0)
    for s in df:
        if s.startswith('MA_'):
            plt_price.plot(t, df[s])
            continue
        if s.startswith('rMAD_'):
            plt_rmads.plot(t, df[s])
            continue
    # if 'pos_opn' in df:
    #     for i in range(len(df)):
    #         time_opn = df.index[i].value
    #         time_clo = df['time_clo'].iloc[i].value
    #         pos_opn = df['pos_opn'].iloc[i]
    #         pos_clo = df['pos_clo'].iloc[i]
    #         if pos_opn == 0:
    #             continue
    #         plt_price.plot([time_opn, time_clo], [pos_opn, pos_clo])
    if 'rprofit' in df:
        plt_rpro = win.addPlot(title='rprofits', row=2, col=0)
        plt_rpro.plot(t, df['rprofit'].fillna(0), symbol='x')
    input()

df = read_data()
df = df[100000:2000000]
print(df.head(1))
df = resample_data(df)
print('dataframe length:',  len(df))
print(df.head(1))

num_mas = 5
calc_MAs(df, num_mas)
print(df.head(1))
calc_rMADs(df)
print(df.head(1))

calc_profits(df)
print(df.head(1))

start_index = 2 ** num_mas
end_index = 9000
cols = [col for col in df if col.startswith('rMAD_')]
test_n = 500
X_train = df.as_matrix(cols)[start_index:end_index]
y_train = df['rprofit'].fillna(0).values[start_index:end_index] > 0
X_test = X_train[-test_n:]
y_test = y_train[-test_n:]
X_train = X_train[:-test_n]
y_train = y_train[:-test_n]
print(np.count_nonzero(y_test))

from sklearn import svm
svc = svm.SVC(kernel='poly', degree=3)
svc.fit(X_train, y_train)
score = svc.score(X_test, y_test)
print('score:', score)
y_pred = svc.predict(X_test)
print(np.count_nonzero(y_pred))



plot_data(df)
