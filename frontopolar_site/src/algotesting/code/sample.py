import pytz
import imp
import pandas as pd
from datetime import datetime
from zipline.algorithm import TradingAlgorithm
import default
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def check_important_columns(data):
    for df in data:
        if 'volume' not in df.axes[1].values:
            default = 10000
            df['volume'] = default
            print "Can't find column 'volume' needed for calculations, " \
                  "column 'volume' with default values(%i) added" % default

        if 'price' not in df.axes[1].values:
            df['price'] = df['close']
            print "Can't find column 'price', column 'close' will be used as price"

def make_panels(universe):
    if universe.parser:
        def parser_func(x):
            return datetime.strptime(x, universe.parser)
        data = [pd.read_csv(filename, index_col=0, date_parser=parser_func) for filename in universe.data_files]
    else:
        data = [pd.read_csv(filename, index_col=0, parse_dates=True) for filename in universe.data_files]

    for dt in data:
        dt.index = dt.index.tz_localize(pytz.UTC)

    check_important_columns(data)

    dict_data = dict()
    for stock, dt in zip(universe.symbols, data):
        dict_data[stock] = dt

    pn = pd.Panel(dict_data)
    training_size = int(pn.shape[1] * universe.training_size)
    training_pn = pn[:, :training_size, :]
    test_pn = pn[:, training_size:, :]
    return training_pn, test_pn

def wrapped_init(context):
    context.panel = training_panel
    if universe.load_file != "":
        if hasattr(user_defined, 'load') and callable(getattr(user_defined, 'load')):
            user_defined.load(universe, context)
        else:
            default.load(universe,context)
    else:
        user_defined.initialize(context)
    if universe.save_file != "":
        if hasattr(user_defined, 'save') and callable(getattr(user_defined, 'save')):
            user_defined.save(universe, context)
        else:
            default.save(universe,context)

class Universe:
    def __init__(self):
        self.algo_filename = ""
        self.data_files = ""
        self.save_file = ""
        self.load_file = ""
        self.frequency = ""
        self.capital_base = 10000
        self.parser = None
        self.symbols = []
        self.training_size = None

    def fill_parameters(self, params):
        paths = []
        for data_filename in params['data_filenames']:
            paths.append(os.path.join(BASE_DIR, 'uploads/datasets/'+data_filename))
        if params['load_file'] != "":
            self.load_file = os.path.join(BASE_DIR, 'uploads/'+params['load_file'])
        if params['save_file'] != "":
            self.save_file = os.path.join(BASE_DIR, 'uploads/'+params['save_file'])
        self.data_files = paths
        self.algo_filename = params['algorithm']
        self.frequency = params['frequency']
        self.capital_base = params['base_capital']
        self.symbols = params['symbols']
        self.parser = params['parser']
        self.training_size = params['train_size']



def handle_algorithm_testing(params):
    global universe, training_panel, test_panel
    universe = Universe()
    universe.fill_parameters(params)
    global user_defined
    algo_filename = universe.algo_filename
    path = os.path.join(BASE_DIR, 'uploads/algorithms/'+algo_filename)
    user_defined = imp.load_source("user_defined", path)

    training_panel, test_panel = make_panels(universe)

    handle_data_1 = user_defined.handle_data

    algo = TradingAlgorithm(initialize=lambda x: wrapped_init(x),
                            handle_data=handle_data_1,
                            data_frequency=universe.frequency,
                            capital_base=universe.capital_base)
    performance = algo.run(test_panel)
    if hasattr(user_defined, 'analyze') and callable(getattr(user_defined, 'analyze')):
        return user_defined.analyze(results=performance, universe = universe)
    else:
        return default.analyze(results=performance, universe = universe)
