import numpy as np
import pandas as pd
from statsmodels.tsa.arima_process import arma_generate_sample


def load_or_make_and_save_data(filename, make_func):
    try:
        data = pd.read_pickle(filename)
        print('loaded data from file', filename)
        return data
    except:
        data = make_func()
        data.to_pickle(filename)
        print('made data and saved to file', filename)
        return data


def calc_dd(prices, max_dd, *, spread=0, print_progress=0):
    colname_dd_price = 'dd_price' # + '_' + str(max_dd)
    colname_dd_date = 'dd_date' # + '_' + str(max_dd)
    colname_dd_profit = 'dd_profit' # + '_' + str(max_dd)
    colname_dd_datediff = 'dd_datediff' # + '_' + str(max_dd)
    colname_dd_profit_speed = 'dd_profit_speed' # + '_' + str(max_dd)
    df = pd.DataFrame(index=prices.index)
    df.loc[:, colname_dd_price] = np.full_like(prices.values, None)
    df.loc[:, colname_dd_date] = np.full_like(df.index.values, None)
    for i, pos_open in enumerate(prices):
        if i > 0 and i % print_progress == 0:
            print('calc_dd, iteration #', i)
        max_price = pos_open * (1 - spread)
        for j, price in enumerate(prices.iloc[i:]):
            price = price * (1 - spread)
            max_price = max(max_price, price)
            drawdown = (max_price - price) / max_price
            if (drawdown > max_dd):
                df[colname_dd_price].values[i] = price
                df[colname_dd_date].values[i] = df.index[i+j]
                # print('break after', j)
                break

    df.loc[:, colname_dd_profit] = (df[colname_dd_price] - prices) / prices
    df.loc[:, colname_dd_datediff] = df[colname_dd_date] - df.index
    df.loc[:, colname_dd_profit_speed] = df[colname_dd_profit] / (df[colname_dd_datediff].dt.total_seconds() / 60 / 60 / 24 / 366)
    return df

def calc_dds(prices, max_dds, *, spread=0, print_progress=0):
    df = pd.DataFrame(index=prices.index)
    for max_dd in max_dds:
        if print_progress:
            print('calculating with max_dd of', max_dd)
        rename_columns_dict = {
            'dd_price': 'dd_price' + '_' + str(max_dd),
            'dd_date': 'dd_date' + '_' + str(max_dd),
            'dd_profit': 'dd_profit' + '_' + str(max_dd),
            'dd_datediff': 'dd_datediff' + '_' + str(max_dd),
            'dd_profit_speed': 'dd_profit_speed' + '_' + str(max_dd)
        }
        subdf = calc_dd(prices, max_dd, spread=spread, print_progress=print_progress)
        subdf.rename(columns=rename_columns_dict, inplace=True)
        df = pd.concat([
            df,
            subdf
        ], axis=1, join_axes=[df.index])

    return df

def calc_rmads(prices, rmads):
    df = pd.DataFrame(index=prices.index)
    # sizes = [2 ** (x + 1) for x in range(num_rmads)]
    for size in rmads:
        df.loc[:, 'ma_' + str(size)] = prices.rolling(size).mean()
        df.loc[:, 'rmad_' + str(size)] = 1 - df['ma_' + str(size)] / prices
    return df


def make_random_df(index):
    arparams, maparams = [1., -1.65851954, 0.69209138], [1, -0.13870413]
    y = arma_generate_sample(arparams, maparams, len(index)) + 100
    return pd.DataFrame(y, index=index, columns=['price'])

def dropna_rows(df):
    first_valid_index = max(map(lambda colname: df[colname].first_valid_index(), df))
    last_valid_index = min(map(lambda colname: df[colname].last_valid_index(), df))
    df = df.loc[first_valid_index:last_valid_index].copy()
    return df