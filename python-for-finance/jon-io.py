import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename = '/home/tot/_tot/projects/data/EUR_USD_Week1.csv'
df = pd.read_csv(filename,
    parse_dates=['time'],
    index_col='time',
    names=['Tid', 'Dealable', 'Pair', 'time', 'bid', 'ask'],
    header=0)
del df['Tid']
del df['Dealable']
del df['Pair']

df = df[:1000]
df = df.resample('1T').mean() # should use ohlc
df.loc[:, 'mean_2T'] = df.rolling('2T').mean()

df.loc[:, 'pos_opn'] = pd.Series(np.zeros(len(df.index)), index=df.index)
df.loc[:, 'pos_clo'] = pd.Series(np.zeros(len(df.index)), index=df.index)
df.loc[:, 'time_clo'] = pd.Series(df.index.copy(), index=df.index)


print(df.head())

now = 20
window_size = now
def update_plot():
    plt.clf()
    simtick()
    window_start = now+1 - window_size
    drawn_df = df[window_start:now+1]
    drawn_df['bid'].plot()
    drawn_df['ask'].plot()
    # plt.plot(drawn_df.loc())
    plt.draw()

def on_keyboard(event):
    global now
    if event.key == 'right':
        now += 1
    elif event.key == 'left':
        now -= 1
    update_plot()

rstoploss = -0.0005
rtakeprofit = 0.0005
oposs = []

def simtick():
    bid = float(df.iloc[now, 0])
    ask = float(df.iloc[now, 1])
    time = df.index[now]
    pos = [time, ask]
    oposs.append(pos)
    i = len(oposs)
    while i > 0:
        i -= 1
        opos = oposs[i]
        rprofit = (opos[1] - bid) / opos[1]
        if rstoploss < rprofit < rtakeprofit:
            continue
        del oposs[i]
        df.loc[opos[0], 2] = opos[1]
        df.loc[opos[0], 3] = bid
        df.loc[opos[0], 4] = time
        # plt.plot([opos[0], time], [opos[1], bid])
    # print('%s: %s' % (now, len(oposs)))


plt.gcf().canvas.mpl_connect('key_press_event', on_keyboard)


# for i in range(1000):
#     now +=1
#     simtick()

print(len(df))
# update_plot()

# plt.show()


