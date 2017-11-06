from quote import *

class Quotes(object):
    def __init__(self):
        self.quote_dict = dict()

    def create_quote(self, symbol):
        if not self.has_key(symbol):
            q = Quote(symbol)
            self.quote_dict[symbol] = q

        return self.quote_dict[symbol]

    def add_quote(self, q):
        if type(q) is not Quote:
            return
        if not self.has_key(q.get_symbol()):
            self.quote_dict[q.get_symbol()] = q

    def has_key(self, symbol):
        return symbol in self.quote_dict.keys()

    def get_quote(self, symbol):
        if self.has_key(symbol):
            return self.quote_dict[symbol]
        else:
            return self.create_quote(symbol)

    def update_1(self, tokens):
        # initialize fields
        # 4 symbol
        q = self.get_quote(tokens[4])
        # 5 last
        if tokens[5] != '0':
            q.set_raw_last(tokens[5])
        # 6 bid
        # 7 bid sz
        q.set_raw_bid(tokens[6])
        q.set_raw_bid_size(tokens[7])
        # 8 ask
        # 9 ask sz
        q.set_raw_ask(tokens[8])
        q.set_raw_ask_size(tokens[9])
        # 10 high
        q.set_raw_high(tokens[10])
        # 11 low
        q.set_raw_low(tokens[11])
        # 12 volume
        q.set_raw_volume(tokens[12])
        # 13 open
        q.set_raw_open(tokens[13])
        # 14 close
        q.set_raw_close(tokens[14])
        # 15 tick value
        # 16 news alert
        q.set_raw_news_alert(tokens[16])
        # 17 VWAP from open
        # 18 10 minute VWAP
        q.set_raw_vwap(tokens[17])
        q.set_raw_vwap_10m(tokens[18])
        pass

    def update_A(self, tokens):
        q = self.get_quote(tokens[4])
        if tokens[5] != '0':
            q.set_raw_ask(tokens[5])
        if tokens[6] != '0':
            q.set_raw_ask_size(tokens[6])

    def update_B(self, tokens):
        q = self.get_quote(tokens[4])
        if tokens[5] != '0':
            q.set_raw_bid(tokens[5])
        if tokens[6] != '0':
            q.set_raw_bid_size(tokens[6])

    def update_C(self, tokens):
        # both bid and ask
        q = self.get_quote(tokens[4])
        if tokens[7] != '0':
            q.set_raw_ask(tokens[7])
        if tokens[8] != '0':
            q.set_raw_ask_size(tokens[8])
        if tokens[5] != '0':
            q.set_raw_bid(tokens[5])
        if tokens[6] != '0':
            q.set_raw_bid_size(tokens[6])

    def update_D(self, tokens):
        # high
        q = self.get_quote(tokens[4])
        q.set_raw_high(tokens[5])

    def update_F(self, tokens):
        q = self.get_quote(tokens[4])
        q.set_raw_open(tokens[5])

    def update_G(self, tokens):
        q = self.get_quote(tokens[4])
        q.set_raw_close(tokens[5])

    def update_H(self, tokens):
        q = self.get_quote(tokens[4])
        q.set_raw_volume(tokens[5])

    def update_J(self, tokens):
        q = self.get_quote(tokens[4])
        if tokens[5] != '0':
            q.set_raw_last(tokens[5])
        if tokens[6] != '0':
            q.set_raw_last_size(tokens[6])

    def update_K(self, tokens):
        # high
        q = self.get_quote(tokens[4])
        q.set_raw_low(tokens[5])


    def update_N(self, tokens):
        # non-official close
        q = self.get_quote(tokens[4])
        q.set_raw_close(tokens[5])

    def update_V(self, tokens):
        q = self.get_quote(tokens[4])
        if tokens[5] != '0':
            q.set_raw_vwap(tokens[5])
        if tokens[7] != '0':
            q.set_raw_vwap_10m(tokens[5])






