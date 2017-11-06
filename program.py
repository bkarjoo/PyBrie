#!/usr/bin/python

import datetime
import msgpack
import multiprocessing as mp
import openpyxl
import threading
import zmq

from ctypes import *
from time import *
from _ctypes import FreeLibrary

from UserInfo import *
from EServerConnection import *

from SessionInfo import *
from HAPI_DLL import *
from order_status_fields import *
from order import *
from submited_orders import *
#from interactive import interactive


def ESMsgHdlr(Msg):
    lMsg = Msg.decode('utf-8')
    # print('ES: ' + lMsg)
    # tokens = lMsg.split(':')
    # if tokens[2] != 'S' and tokens[2] != 'P' and tokens[2] != 'A' \
    #         and tokens[2] != 'L' and tokens[2] != 'D' and tokens[2] != 'B':
    #     print(lMsg)
    # global login_complete
    # if tokens[eMsgHdr.MsgType] == 'A':
    #     login_complete = True
    # global acct
    # # print(tokens[2])
    # if tokens[4] == acct:
    #     print('ES: '+lMsg)
    global ES
    ES.HandleESMsg(lMsg)


def ISMsgHdlr(Msg):
    lMsg = Msg.decode('utf-8')
    # print('IS: ' + lMsg)
    global IS
    IS.HandleISMsg(lMsg)


# cleanup callbacks during exit
def CleanUpES():
    # print ('cleanup called')
    global ES
    # print (ES.IsConnected())

    ES.OnDisconnect()


def CleanUpIS():
    print('IS: disconnect')

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)

    def run(self):
        print "Starting "
        while keep_running:
            print("hello")
            sleep(1)
        print "Ending"


def Interactive():
    global ES
    global IS
    MyUI = ES.uiES
    while True:
        cmd = raw_input('Enter NO for New Order\n POS for Position List\n IS for Market Data\n Q to Quit\n')
        if cmd == 'Q' or cmd == 'q' or cmd == 'Quit':
            break

        if cmd == 'NO':
            print ("== ES: NEW ORDER ==")

            while True:
                Acct = raw_input("ES NO: Enter Account (ACCT to list): ")
                if Acct == '' or Acct == 'list':
                    continue

                if Acct == "ACCT":
                    lAccts = ''
                    for i in MyUI.Accts:
                        lAccts += i + ' '
                    print ("ES ACCTS: " + lAccts)
                else:
                    break

                    # so i have no accts in the list
                    # and i don't see anywhere that actually populates this list

                    # so this isn't actually doing anythign with my input
                    # nvm, stored in Acct

            Symb = raw_input("ES NO: Enter Symbol: ")

            while True:
                Side = raw_input("ES NO: Enter Side(B/S/T): ")
                if Side == 'B' or Side == 'S' or Side == 'T':
                    break

            while True:
                sQty = raw_input("ES NO: Enter Qty: ")
                if int(sQty) > 0:
                    break

            while True:
                sPr = raw_input("ES NO: Enter Price: ")
                if float(sPr) > 0.0:
                    break

            while True:
                Chan = raw_input("ES NO: Enter Channel (CHAN to list): ")
                if Chan == "CHAN":
                    ES.GetAvailChan()
                else:
                    break

            TIF = raw_input("ES NO: TIF: ")
            if TIF == '':
                TIF = 'DAY'

            while True:
                OType = raw_input("ES NO: Order Type (L/M): ")
                if OType == 'L' or OType == 'M':
                    break

            OK2Snd = raw_input("ES NO: Send (Y/N): ")

            if OK2Snd == 'Y' or OK2Snd == 'YES':
                ES.SendESOrderMsg(sAcct=Acct, sSymb=Symb, sSd=Side, sQty=sQty, sPr=sPr, sContra='', sChan=Chan,
                                  sTIF=TIF, sOType=OType, sDisp='Y')
            continue

        if cmd == 'POS':

            while True:
                Acct = raw_input("ES POS: Enter Account (ACCT to list): ")
                if Acct == "ACCT":
                    lAccts = ''
                    for i in MyUI.Accts:
                        lAccts += i + ' '
                    if lAccts != '':
                        lAccts += 'ALL'
                    print ("ES ACCTS: " + lAccts)
                else:
                    break

            ES.PrintPositionsList(Acct)
            continue

        if cmd == 'ISFL':
            filtr = raw_input("IS: FILTER: ")
            IS.filter.append(filtr)
            continue
        if cmd == 'ISFLLIST':
            filtr = raw_input("IS: LIST FILTER (MAX {0}): ".format(len(IS.filter)))
            for i in IS.filter:
                print('IS FLTR: ' + i)
            continue

        if cmd == 'CANCEL':
            while True:
                order_to_cxl = raw_input('Enter Order Number: ')
                if order_to_cxl != '':
                    break


        if cmd == 'IS':
            if IS.IsConnected() == 0:
                print('IS Connection currently is DOWN.')
                continue

            ECN = 'ALL'
            print('== ISERVER REQUESTS ==')
            while True:
                Symb = raw_input("SYMB: ")
                if (Symb != ""):
                    break

            while True:
                DataType = raw_input("Data Type (1-4,6): ")

                if (DataType == '1' or DataType == '2' or \
                                DataType == '3' or DataType == '4' or DataType == '6'):

                    if DataType == '3':
                        while True:
                            ECN = raw_input("ECN Chan:")
                            if ECN != '':
                                ECN = 'ALL'
                            break

                break

            while True:
                AddRem = raw_input("Add or Remove Symb (A/R): ")
                if (AddRem == 'A' or AddRem == 'R' or DataType == '6'):
                    break

            IS.AddRemDataSub(Symb, AddRem, DataType, ECN)
            continue

        if cmd == 'es_status':
            if ES.IsConnected():
                print("ES is connected.")
            else:
                print("ES is not connected.")

        if cmd == 'is_status':
            if IS.IsConnected():
                print("IS is connected.")
            else:
                print("IS is not connected.")

        if cmd == 'quote':
            quote_ticker = raw_input("Enter symbol: ")
            IS.PrintTicker(quote_ticker)

def main():
    # Create new threads
    # thread1 = myThread(1,"t1",1)

    # global login_complete
    # login_complete = False

    # Start new Threads
    # global keep_running
    # keep_running = True
    # thread1.start()
    global acct

    # HSI = HySessionInfo(b"algogroup", b"algogroup", b"10.17.240.155", 8701)
    # acct = 'ALGOPAIR'
    HSI = HySessionInfo(b"demo", b"demo", b"10.17.240.159", 7620)
    acct = 'DEMOX1'

    ESHdlr = SessionInfo.fnMsgHdlr_t(ESMsgHdlr)
    ISHdlr = SessionInfo.fnMsgHdlr_t(ISMsgHdlr)
    ESClUp = SessionInfo.fnCleanUp_t(CleanUpES)
    ISClUp = SessionInfo.fnCleanUp_t(CleanUpIS)

    SI = SessionInfo(addressof(HSI), ESHdlr, ISHdlr, ESClUp, ISClUp)
    HAPI = HAPI_DLL(".\\HAPIKIT.DLL", SI)
    HAPI.Run()
    global ES
    global IS
    ES.set_print_on(False)
    sleep(2)



    Interactive()
    print("Out of interactive.")

    # while ES.IsConnected() == False:
    #     print('waiting for login')
    #     sleep(1)
    # else:
    #     print('Connected')
    #     # if I don't wait here order will not go through
    #     sleep(10)
    #
    #
    #
    # #sleep(1000)
    # # keep_running = False
    #
    #
    # print("Entering the loop")
    #
    # i = 0
    # while True:
    #     sleep(5)
    #     print(ES.IsConnected())
    #     if ES.IsConnected():
    #         print("CONNECTED -- ")
    #     else:
    #         print("NOT CONNECTED -- ")
    #     print("ATEMPT SENDING ORDER")
    #     o1 = order(1,'SPY',252)
    #     o1.submit(ES)
    #     i = i + 1
    #     if i == 1:
    #         break
    # #
    ES.Exit()

    sleep(1)
    print "Exiting Main Thread"


if __name__ == "__main__":
    main()

