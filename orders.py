from order import *
from message import *

class orders(object):
    def __init__(self):
        self.by_parrent = dict()
        self.by_id = dict()

    def add_order(self, ord):
        if type(ord) == order:
            if (ord.parrent_id()) != '':
                self.by_parrent[ord.parrent_id()] = ord

    def update_order(self, msg):
        if type(msg) == message:
            id = msg.order_id()
            pid = msg.parrent_id()
            o = order()
            if id != '':
                if not id in self.by_id:
                    if pid != '':
                        o = self.by_parrent[pid]
                        self.by_id[id] = o
                else:
                    o = self.by_id[id]
            o.update(msg)


