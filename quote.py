class Quote(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.bid = '0.0'
        self.ask = '0.0'
        self.bid_sz = '0'
        self.ask_sz = '0'
        self.open = '0.0'
        self.close = '0.0'
        self.volume = '0'
        self.last = '0.0'
        self.last_sz = '0'
        self.subscribed = False
        self.vwap = '0.0'
        self.vwap_10m = '0.0' 
        self.high = '0.0'
        self.low = '0.0'
        self.news_alert = '0'

    def handle_message(self, msg):
        tokens = msg.split(':')
        type = tokens[2]
        if type == 'A':
            if self.ask != tokens[5]:
                self.ask = tokens[5]
            if tokens[6] != '0' and self.ask_sz != tokens[6]:
                self.ask_sz = tokens[5]

    def get_symbol(self):
        return self.symbol

    def get_raw_ask(self):
        return self.ask

    def set_raw_ask(self, value):
        self.ask = value

    def get_ask(self):
        return float(self.ask)

    def get_raw_ask_size(self):
        return self.ask_sz

    def set_raw_ask_size(self, value):
        self.ask_sz = value

    def get_ask_size(self):
        return int(self.ask_sz)

    def get_raw_bid(self):
        return self.bid

    def set_raw_bid(self, value):
        self.bid = value

    def get_bid(self):
        return float(self.bid)

    def get_raw_bid_size(self):
        return self.bid_sz

    def set_raw_bid_size(self, value):
        self.bid_sz = value

    def get_bid_size(self):
        return int(self.bid_sz)

    def get_raw_open(self):
        return self.open

    def set_raw_open(self, value):
        self.open = value

    def get_open(self):
        return float(self.open)
    
    def get_raw_close(self):
        return self.close

    def set_raw_close(self, value):
        self.close = value

    def get_close(self):
        return float(self.close)

    def get_raw_volume(self):
        return self.volume

    def set_raw_volume(self, value):
        self.volume = value

    def get_volume(self):
        return int(self.volume)
    
    def get_raw_news_alert(self):
        return self.news_alert

    def set_raw_news_alert(self, value):
        self.news_alert = value

    def get_news_alert(self):
        return int(self.news_alert)

    def get_raw_last(self):
        return self.last

    def set_raw_last(self, value):
        self.last = value

    def get_last(self):
        return float(self.last)

    def get_raw_last_size(self):
        return self.last_sz

    def set_raw_last_size(self, value):
        self.last_sz = value

    def get_last_size(self):
        return float(self.last_sz)

    def get_raw_vwap(self):
        return self.vwap

    def set_raw_vwap(self, value):
        self.vwap = value

    def get_vwap(self):
        return float(self.vwap)
     
    def get_raw_vwap_10m(self):
        return self.vwap_10m

    def set_raw_vwap_10m(self, value):
        self.vwap_10m = value

    def get_vwap_10m(self):
        return float(self.vwap_10m)

    def get_raw_high(self):
        return self.high

    def set_raw_high(self, value):
        if value != '0':
            self.high = value

    def get_high(self):
        return float(self.high)
    
    def get_raw_low(self):
        return self.low

    def set_raw_low(self, value):
        if value != '0':
            self.low = value

    def get_low(self):
        return float(self.low)

    def __str__(self):
        return self.symbol + ':'  \
            + ' bid: ' + self.bid \
            + ' ask: ' + self.ask \
            + ' bid_sz: ' + self.bid_sz \
            + ' ask_sz: ' + self.ask_sz \
            + ' open: ' + self.open \
            + ' close: ' + self.close \
            + ' volume: ' + self.volume \
            + ' last: ' + self.last \
            + ' last_size: ' + self.last_sz \
            + ' vwap: ' + self.vwap \
            + ' vwap_10m: ' + self.vwap_10m \
            + ' high: ' + self.high \
            + ' low: ' + self.low \
            + ' news: ' + self.news_alert

