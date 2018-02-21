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

def normalize_data(df):
    '''
    Normalize data using the first row of the dataframe
    '''
    return df/df[0, :]   # df[0, :]  means all columns in row[0]


def plot_data(df, title="Stock prices"):
    ax = df.plot(title = title, fontsize=2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()

def plot_selected(df, columns, start_index, end_index):
    df_selected = df.ix[start_index: end_index, columns]
    df_selected.plot()
    plt.show()


def test_run():
    # define date range
    start_date = '2010-01-22'
    end_date = '2010-10-26'
    dates = pd.date_range(start_date, end_date)

    # Choose stock symbols to read
    symbols = ['GOOG', 'IBM', 'GLD']
    
    # Get stock data
    df = get_data(symbols, dates)
    
    # slice by row using .ix[]
    df_slice = df.ix['2010-01-01': '2010-01-31']

    # slice by column
    df_slice = df['GOOG']
    df_slice = df[['IBM', 'GLD']]

    # slice by row and column
    df_slice = df.ix['2010-01-01': '2010-01-31', ['IBM', 'GLD']]

if __name__ == "__main__":
    test_run()
