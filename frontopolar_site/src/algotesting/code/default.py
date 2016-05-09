import pytz
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from zipline.algorithm import TradingAlgorithm
from zipline.api import order, record, symbol


# Define algorithm
def initialize(context):
    # Here we can use data from csv and write learned parameters into context's fields.
    context.panel  # Panel with training data.
    context.result = 12  # Here we can save result for serialization.
    context.previous = 0


def handle_data(context, data):
    context.panel  # Here we have access to training data also.
    # Make solution using the result of learning:
    if not int(data[symbol('AAPL')].price) % context.result:
        order(symbol('AAPL'), 10)
    # Record some values for analysis in 'analyze()'.
    sids = context.panel.axes[0].values
    prices = [data[symbol(sid)].price for sid in sids]
    record(Prices=prices)
    record(Prediction=3 * data[symbol('AAPL')].price - 2.2 * context.previous)
    # Record current price to use it in future.
    context.previous = data[symbol('AAPL')].price

def load(universe, context):
    context.result = pd.read_pickle(universe.load_file)

def save(universe, context):
    pd.to_pickle(context.result, universe.save_file)

def analyze(results, universe):
    f, (ax1, _) = plt.subplots(1, 2)
    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value (USD)')
    f.text(.02, .02, "Max portfolio value:{}\nMin portfolio value:{}\nEarned money:{}".format(results.portfolio_value.max(),
                    results.portfolio_value.min(), results.portfolio_value.iloc[-1] - results.portfolio_value.iloc[0]))
    plt.legend()
    return f