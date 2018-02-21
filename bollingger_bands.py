import os
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 

def symbol_to_path(symbol, base_dir='data'):
    return os.path.join(base_dir, '{}.csv'.format(str(symbol)))

def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        # TODO: Read and join data for each symbol
        path = symbol_to_path(symbol)
        df_tmp = pd.read_csv(path, index_col="Date", parse_dates=True,
                         usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_tmp = df_tmp.rename(columns={'Adj Close':symbol})
        # or use inner join to drop the NaN values
        df = df.join(df_tmp, how='inner')
    return df

def get_rolling_mean(values, window):
    return pd.rolling_mean(values, window = window)

def get_rolling_std(values, window):
    return pd.rolling_std(values, window = window)

def get_bollinger_bands(rm, rstd):
    upper_band = rm + rstd * 2
    lower_band = rm - rstd * 2
    return upper_band, lower_band

def test_run():
    # define date range
    start_date = '2010-01-22'
    end_date = '2010-10-26'
    dates = pd.date_range(start_date, end_date)

    # Choose stock symbols to read
    symbols = ['SPY']
    
    # Get stock data
    df = get_data(symbols, dates)

    # compute bollinger bands
    # 1. Compute rolling mean
    rm_SPY = get_rolling_mean(df['SPY'], window=20)

    # 2. Compute rolling standard deviation
    rstd_SPY = get_rolling_std(df['SPY'], window=20)

    # 3. Compute uppter and lower bands
    upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)

    # Plot raw SPY values, rolling mean and bollinger bands
    ax = df['SPY'].plot(title='Bollinger Bands', label='SPY')
    rm_SPY.plot(label="Rolling mean", ax=ax)
    upper_band.plot(label="Upper band", ax=ax)
    lower_band.plot(label="Lower band", ax=ax)
    plt.show()

if __name__ == "__main__":
    test_run()
