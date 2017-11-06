import quandl

class fields:
    ticker = 'ticker'
    date = 'date'
    open = 'open'
    high = 'high'
    low = 'low'
    close = 'close'
    volume = 'volume'
    exdividend = 'ex-dividend'
    split_ratio = 'split_ratio'
    adj_open = 'adj_open'
    adj_high = 'adj_high'
    adj_low = 'adj_low'
    adj_close = 'adj_close'
    adj_volume = 'adj_volume'

def get_day_data(dd, symb):
    return quandl.get_table('WIKI/PRICES', date = dd, ticker = symb)

class strategy(object):
    """
    each symbol will be traded independently
    """
    def __init__(self, symbol):
        self.symbol = symbol

    def feed_data(self, line):
        qdata = get_day_data(line[0], line[1])
        #print(line)
        if qdata.empty:
            return
        else:
            print(line[0],line[1],round(qdata[fields.open][0],2),round(qdata[fields.close][0],2),round(qdata[fields.volume][0],0))


strat_dict = dict()




quandl.ApiConfig.api_key = 'zwwkVz1fAy6HaFLjcJdn'

# table = get_day_data('2000-01-03','YHOO')

def run():

    with open('C:\\Users\\b.karjoo\\Downloads\\TRESS.csv') as f:
        header = f.readline()[:-1].split(',')

        while True:
            line = f.readline()[:-1].split(',')
            strat = None

            if strat_dict.has_key(line[1]):
                strat = strat_dict[line[1]]
            else:
                strat = strategy(line[1])
                strat_dict[line[1]] = strat
            strat.feed_data(line)



    f.close()


run()
