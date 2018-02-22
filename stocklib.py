import os
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 

def symbol_to_path(symbol, base_dir='data'):
    return os.path.join(base_dir, '{}.csv'.format(str(symbol)))

def get_data(symbols, dates):
    """
    Read stock data (adjusted close) for given symbols from CSV files.
    Usage:
        # define date range
        start_date = '2010-01-22'
        end_date = '2010-10-26'
        dates = pd.date_range(start_date, end_date)

        # Choose stock symbols to read
        symbols = ['SPY']
        
        # Get stock data
        df = get_data(symbols, dates)
    """
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        path = symbol_to_path(symbol)
        df_tmp = pd.read_csv(path, index_col="Date", parse_dates=True,
                         usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_tmp = df_tmp.rename(columns={'Adj Close':symbol})
        # or use inner join to drop the NaN values
        df = df.join(df_tmp, how='inner')
    return df

def get_rolling_mean(values, window):
    '''
    rm_SPY = get_rolling_mean(df['SPY'], window=20)
    '''
    return pd.rolling_mean(values, window = window)

def get_rolling_std(values, window):
    '''
    rstd_SPY = get_rolling_std(df['SPY'], window=20) 
    '''
    return pd.rolling_std(values, window = window)

def get_bollinger_bands(rm, rstd):
    upper_band = rm + rstd * 2
    lower_band = rm - rstd * 2
    return upper_band, lower_band


def compute_daily_returns(df):
    '''
    daily_return = (price[t] / price[t-1]) - 1
    '''
    daily_returns = df.copy()
    # df[1:] picks all the rows from 1 till the end
    # df[:-1] picks all the rows from 0 till 1 less than the end
    # when given two df, pandas will try to match each row based on index when performing element-wise operations
    daily_returns[1:] = (df[1:]/df[:-1].values) - 1
    # set daily returns for row 0 to 0
    daily_returns.ix[0, :] = 0

    ## or
    # daily_returns = (df/df.shift(1)) - 1
    # daily_returns.ix[0, :] = 0   # Pandas leaves the 0th row full of NaNs
    return daily_returns
    