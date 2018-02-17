import os
import pandas as pd

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


def test_run():
    # define date range
    start_date = '2010-01-22'
    end_date = '2010-10-26'
    dates = pd.date_range(start_date, end_date)

    # Choose stock symbols to read
    symbols = ['GOOG', 'IBM', 'GLD']
    
    # Get stock data
    df = get_data(symbols, dates)
    print df


if __name__ == "__main__":
    test_run()
