# remember: c:/Python27x86/Scripts/pip.exe install msgpack-python to install packages
import msgpack
import multiprocessing as mp
import zmq

from ctypes import *

class IServerConnection:

    def __init__(self):
        self.filter = []
        self.bid_ask_dict = {} # ticker
        self.previously_connected = False

    def setHAPI(self, HAPI):
        self.HAPI = HAPI

    def HandleISMsg(self, orig_msg):
        msg = orig_msg.split(':')
        ticker = msg[4]
        msg_type = msg[2]

        bid = ''
        ask = ''
        bid_sz = ''
        ask_sz = ''
        if msg_type in ['A', 'B', 'C']:
            if msg_type == 'A': # strlen of 6 denotes px chg rather than just size chg
                ask = msg[5]
                ask_sz = msg[6]
            elif msg_type == 'B':
                bid = msg[5]
                bid_sz = msg[6]
            elif msg_type == 'C':
                bid = msg[5]
                ask = msg[7]
                bid_sz = msg[6]
                ask_sz = msg[8]

            # if bid != '':
            #     self.bid_ask_dict[ticker]['bid'] = float(bid)
            # if ask != '':
            #     self.bid_ask_dict[ticker]['ask'] = float(ask)
            #
            #
            # if bid_sz != '': # kept separate from above since updates can have chg in sz but not px
            #     self.bid_ask_dict[ticker]['bid_sz'] = int(bid_sz) * 100 # in hundreds per spec/david
            # if ask_sz != '':
            #     self.bid_ask_dict[ticker]['ask_sz'] = int(ask_sz) * 100
            
    def IsConnected(self):
        c_uint_p = POINTER(c_uint)
        rv = self.HAPI.dll.GetISConnState()
        if rv == 0: return 0
        return cast(rv, c_uint_p).contents.value

    def PrintTicker(self, ticker):
        print('fetching quotes for ', ticker)
        try:
            print('bid: ', self.bid_ask_dict[ticker]['bid'])
        except:
            print('bid not found')

        try:
            print('ask: ', self.bid_ask_dict[ticker]['ask'])
        except:
            print('ask not found')

        try:
            print('bid_sz: ', self.bid_ask_dict[ticker]['bid_sz'])
        except:
            print('symbol not found')

        try:
            print('ask_sz: ', self.bid_ask_dict[ticker]['ask_sz'])
        except:
            print('symbol not found')

    def AddRemDataSub(self, symb, ar, msg_type, ecn = 'ALL'):
        if self.IsConnected() == 0:
            if self.previously_connected == True:
                print("IS: Connection is DOWN. trying to reconnect...")
                self.ReconnectSvr()
            else:
                print 'IS: Connection NOT YET UP'
            return
        else:
            self.previously_connected = True

        msg = ""
        if msg_type == '1':
            msg = "#:00000:1:000:{0}:{1}:*".format( symb, ar )

        if msg_type == '2':
            msg = "#:00000:2:000:{0}:{1}:Y:*".format( symb, ar )

        if msg_type == '3':
            msg = "#:00000:3:000:{0}:{1}:{2}:*".format( symb, ecn, ar )

        if msg_type == '4':
            msg = "#:00000:4:000:{0}:0:{1}:*".format( symb, ar )

        if msg_type == '6':
            msg = "#:00000:6:000:{0}:*".format( symb )
            
        if msg == '':
            return

        self.bid_ask_dict[symb] = {'bid': None, 'ask': None}

        RVal    = self.HAPI.dll.SendMsgIS(msg.encode())
        print ("IS: Subscribe={0} - {1}".format(RVal, msg))

