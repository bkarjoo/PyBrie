import time
import datetime
import msgpack
import zmq

from UserInfo import *
from ctypes import *


ADMMSG_RECONNECT = 1001
ADMMSG_TRACE_TOGGLE = 1002
DEF_DISP_QTY = 100

class EServerConnection:

    def __init__(self):
        self.nLastParent = 0
        self.uiES = UserInfo()
        self.sDefAcct = ''
        self.nParentIDs = []
        self.nLastParent = 0
        self.print_on = True

        context = zmq.Context()
        pub = context.socket(zmq.PUB)
        port = pub.bind_to_random_port('tcp://*')

        self.pub = pub
        self.url = 'tcp://127.0.0.1:' + str(port)

        self.U_flag = False
        self.previously_connected = False


        # EXPERIMENTAL
        self.session_start_timestamp = datetime.datetime.now()
        self.cur_buying_power = 1000 # B, T orders reduce BP by same amt. BC, S orders do NOTHING to BP

    def set_print_on(self, on_off_bool):
        self.print_on = on_off_bool

    def setHAPI(self, HAPI):
        self.HAPI = HAPI

    def getNextID(self):
        nLastParent = self.nLastParent
        nParentIDs = self.nParentIDs
        nLastParent += 1
        nRet = nLastParent
        nParentIDs.append( nLastParent )
        return nLastParent

    def popParent(self, nPID ):
        try:
            if self.nLastParent < nPID:
                self.nLastParent = nPID

            self.nParentIDs.remove(nPID)
        except:
            #print("ParentID {0} was not used".format( nPID ))
            pass

            # getting this a lot on startup for some reason
            # why?

    def HandleESMsg(self,lMsg):
        msg = lMsg.split(':')

        if msg[eMsgHdr.MsgType] == 'S' and msg[4] == 'S' and msg[14] == 'L':
            pass
        elif msg[eMsgHdr.MsgType] == 'F' and msg[4] in ['E', 'X']:
            pass
        elif msg[ eMsgHdr.MsgType ] in ['U','D','L','A','P']:
            pass
        elif not self.U_flag: # TURN OFF message REPLAY!:
            return


        # END of Login
        if msg[ eMsgHdr.MsgType ] == 'U': #End of Login
            if self.print_on:
                print('ES: -------------------- ES Login Processing done -----------------\n')

            self.U_flag = True # replay done

        #Account Msg
        if msg[ eMsgHdr.MsgType ] == 'A': 

            self.uiES.Accts[ msg[ eMsgAcct.ID ] ]        = Accounts(     msg[ eMsgAcct.ID ],
                                                                            msg[ eMsgAcct.BP ],
                                                                            msg[ eMsgAcct.RBP ],
                                                                            msg[ eMsgAcct.ATyp ],
                                                                            msg[ eMsgAcct.FirmID ] )
            #setting first one as default, if there are more than or not
            if len(self.uiES.Accts) == 1: 
                self.sDefAcct = msg[ eMsgAcct.ID ]

            self.cur_buying_power = float(msg[6])
            #print("ES: Acct, " + msg[ eMsgAcct.ID ] + " added.  Account Dictionary Sz: %d" % len(self.uiES.Accts) )


        #OvNight Pos - 2 keys: Acct, Symb to look up Position
        # i get this upon login to send me my opening positions, if any
        if msg[ eMsgHdr.MsgType ] == 'P': 
            SymbPos     =   self.uiES.OvPos.get( msg[ eMsgONPos.ACCT ] )
            if( SymbPos == None ):
                Pos     =   Position(  msg[ eMsgONPos.ACCT ],
                                        msg[ eMsgONPos.SYMB ],
                                        int( msg[ eMsgONPos.ONQTY ] ),
                                        float( msg[ eMsgONPos.ONPR ] ) )
                self.uiES.OvPos[msg[eMsgONPos.ACCT]] = { msg[ eMsgONPos.SYMB ] : Pos }
            else:
                Pos     = SymbPos.get( msg[ eMsgONPos.SYMB ] )
                if Pos == None:
                    Pos     =   Position(  msg[ eMsgONPos.ACCT ],
                                            msg[ eMsgONPos.SYMB ],
                                            int( msg[ eMsgONPos.ONQTY ] ),
                                            float( msg[ eMsgONPos.ONPR ] ) )
                else:
                    Pos.Qty = int( msg[ eMsgONPos.ONQTY ] )
                    Pos.Pr  = float( msg[ eMsgONPos.ONPR ] )
                
                # my edit
                self.uiES.OvPos[msg[eMsgONPos.ACCT]][msg[ eMsgONPos.SYMB]] = Pos


            #print("ES: OvNgPos {0} - {1} {2} {3}".format( Pos.Acct, Pos.Symb, Pos.Qty, Pos.Pr ) )


        # NEW ORDER processing
        if  msg[ eMsgHdr.MsgType ] == 'S' and msg[ 4 ] == 'F':
        
            #checking if OrderID exist
            ticker = msg[10]
            sAcct = msg[8]
            sOrdId = msg[9]


            # if self.uiES.Ords.get(sAcct) == None:
           #      self.uiES.Ords[sAcct] = {'': {'': None}} # ticker, orderid: order

            if self.uiES.Ords.get(sAcct) == None:
                self.uiES.Ords[sAcct] = {ticker: {'buy': None, 'sell': None}} 

            if msg[11] in ['B', 'BC']:
                key = 'buy'
            else:
                key = 'sell'

            #:19193:S:104:F:N:0:20170109 151309:DEMOX1:500041:GDX:S:716:22.63::CSFB:AUTO::L::Y: :0:0:d:-1:9,,,,,:S:

            NOrd                    =   Order  (    msg[6], msg[7], msg[8], msg[9],     #parent, timest, acct, orderid
                                                    msg[10], msg[11], int(msg[12]), float(msg[13]), #symb, side, qty, pr
                                                    msg[14], msg[15], msg[16], msg[18], #Cntra, Chan, TIF, OrdType
                                                    msg[19], msg[20], msg[21], msg[22], #MinQty, Disp, Peg Type, Peg Off,
                                                    msg[23], msg[24], msg[25], msg[26], #DiscOff, MaxFlr, TickID, Algo,
                                                    msg[27] )                           #OrigSd
            self.uiES.Ords[sAcct][ticker][key] = NOrd
            self.popParent( int(msg[6]) )

            if (self.print_on):
                print 'NEW ORDER {0}: {1} {2} {3} @ {4}'.format(sOrdId, NOrd.Side, NOrd.Qty, NOrd.Symb, NOrd.Pr)
            # print("ES: S New Order Acct {0} OrderID {1} - sz {2} {3} ".format(sAcct, 
           #      sOrdId, len(self.uiES.Ords), len(self.uiES.Ords[sAcct][ticker])))  





        # ORDER STATUS Processing
        if  msg[ eMsgHdr.MsgType ] == 'S' and msg[ 4 ] == 'S':
            sAcct = msg[7]
            sOrdId = msg[8]
            sSubId = msg[9]
            sChan = msg[13]
            sStat = msg[14]
            ticker = msg[16]
            side = msg[17]


            if side in ['B', 'BC']:
                key = 'buy'
            else:
                key = 'sell'


            # if self.uiES.Ords.get(sAcct) == None:
           #      self.uiES.Ords[sAcct] = {'': {'': None}} # ticker, orderid: order

            if self.uiES.Ords.get(sAcct) == None:
                self.uiES.Ords[sAcct] = {ticker: {'buy': None, 'sell': None}}


            mpOrd = self.uiES.Ords[sAcct].get(ticker)

            # so what if this thing is NONE
            # which is what happens it seems

            nLstQty             = int( msg[10] )
            nLstPr              = float( msg[11] )

            # i moved this
            if  sStat == 'L':
                SymbPos = self.uiES.OvPos.get( sAcct ) #search position by 
                
                if SymbPos != None:
                    Pos = SymbPos.get(ticker)
                    if Pos != None:
                        #Pos.LocInf.AddedQty( nLstQty )
                        self.uiES.OvPos[sAcct][ticker].LocInf.AddedQty( nLstQty )
                    else:
                        Pos = Position( sAcct, ticker, 0, 0.0, LocateInfo( nLstQty ) )
                        self.uiES.OvPos[sAcct][ticker] = Pos
                    #print( 'ES: S Locate Symb={0} Total={1} Avail={2}'.format(ticker, Pos.LocInf.nQtyTot, Pos.LocInf.nQtyAvail ) )
                else:
                    Loc = LocateInfo( nLstQty )
                    self.uiES.OvPos[ sAcct ] = {ticker: Position( sAcct, ticker, 0, 0.0, Loc ) }
                    #print( 'ES: S Locate Symb={0} Total={1} Avail={2}'.format(ticker, Loc.nQtyTot, Loc.nQtyAvail ) )


                if self.uiES.Locates.get(sAcct) == None: # this is a fix for locates dict initialization
                    self.uiES.Locates[sAcct] = {'': None}
                if self.uiES.Locates[sAcct].get(ticker) == None:
                    self.uiES.Locates[sAcct][ticker] = LocateInfo( nLstQty )




            if mpOrd == None or (mpOrd['buy'] == None and mpOrd['sell'] == None): #if mpOrd == None:
                pass
                #print( 'WARNING - Order Status msg ({0}-{1}) has No Parent Order Info'.format( sOrdId, sSubId ) )
            else:
                #Ord                 = mpOrd.get( sOrdId )
                Ord = mpOrd[key]
                

                if Ord == None:
                    pass
                    #print( 'WARNING - Order Status msg ({0}-{1}) has No Parent Order Info'.format( sOrdId, sSubId ) )
                else:

                    sz = Ord.nLvsQty
                    px = Ord.Pr
                    side = Ord.Side

                    #print( "ES: S Status Msg Acct " + sAcct + " OrderID "+ sOrdId + '-' + sSubId + '\n' )


                    # if stat is Cancel
                    if sStat == 'C':
                        # self.uiES.Ords[sAcct][ticker][sOrdId].nLvsQty = 0 # set leaves to 0. useless calc if deleting
                       #  del self.uiES.Ords[sAcct][ticker][sOrdId]

                        self.uiES.Ords[sAcct][ticker][key] = None

                        if Ord.Side == 'T' and Ord.Symb not in self.uiES.ETB: # replenish locates if not in etb list
                            self.uiES.OvPos[sAcct][ticker].LocInf.Buying(nLstQty)

                        if self.print_on:
                            print 'CANCELED order {0} ({1} {2} {3} @ {4})'.format(sOrdId, side, sz, ticker, px)

                    # if stat is Execution
                    if sStat == 'E':
                        # self.uiES.Ords[sAcct][ticker][sOrdId].AddExecution( nLstQty, nLstPr ) # changes cumqty, lvsqty and avgpr
                        # if self.uiES.Ords[sAcct][ticker][sOrdId].nLvsQty == 0: # if no longer active since filled
                       #      del self.uiES.Ords[sAcct][ticker][sOrdId]

                        
                        self.uiES.Ords[sAcct][ticker][key].AddExecution( nLstQty, nLstPr )
                        if self.uiES.Ords[sAcct][ticker][key].nLvsQty == 0:
                            self.uiES.Ords[sAcct][ticker][key] = None

                        

                        Sign = 1
                        if Ord.Side == 'S' or Ord.Side == 'T':
                            Sign = -1
                    
                        SymbPos = self.uiES.OvPos.get( sAcct ) #search position by 
                        if SymbPos != None: # if already have some position in this ticker
                            Pos = SymbPos.get(ticker)
                            if Pos != None:
                                if Ord.Side == 'B' or Ord.Side == 'BC':
                                    Pos.LocInf.Buying( nLstQty ) # adds only if tot loc qty is there up to... if negative, it adds back
                            
                                # change current open pos info
                                if (Pos.Qty + Sign * nLstQty) != 0:
                                    Pos.Pr = ( Pos.Qty * Pos.Pr + Sign * nLstQty * nLstPr ) / (Pos.Qty + Sign * nLstQty)
                                else:
                                    Pos.Pr = 0.0

                                Pos.Qty += Sign * nLstQty
                            else:
                                Pos = Position( sAcct, ticker, Sign * nLstQty, Sign * nLstPr )
                            
                            self.uiES.OvPos[sAcct][ticker] = Pos

                        else: # if no position yet. 
                            Pos = Position( sAcct, ticker, Sign * nLstQty, Sign * nLstPr )
                            self.uiES.OvPos[ sAcct ] = {ticker: Pos }


                        # nlstqty seems funny
                        #
                        # SENDING ORDER: B 3 GDX @ 22.65
                        # NEW ORDER 1218073: B 3 GDX @ 22.65
                        # ACTIVE THREAD GOT PASSIVE EXECUTION
                        # SENDING ORDER: B 7 GDX @ 22.65
                        # NEW ORDER 1218074: B 7 GDX @ 22.65
                        # EXECUTION: B 3 GDX @ 22.65. LEAVES: 4. POSITION: 3
                        # EXECUTION: B 7 GDX @ 22.65. LEAVES: -3. POSITION: 10

                        # was this a timing thing then
                        # seems like i got a passive execution while i had a 



                        self.pub.send_multipart([msgpack.packb(ticker), msgpack.packb(Sign * nLstQty)]) # send to active worker thread
                        if self.print_on:
                            print 'EXECUTION: {0} {1} {2} @ {3}. LEAVES: {4}. POSITION: {5}'.format(Ord.Side, nLstQty, ticker, nLstPr, Ord.nLvsQty, Pos.Qty)
                        #print("ES: Position [{0}:{1}] = {2} shr {3} pr".format( Pos.Acct, Pos.Symb, Pos.Qty, Pos.Pr ) )
                
        # AWAY MPIDs
        if  msg[ eMsgHdr.MsgType ] == 'D':
            self.uiES.Aways[ msg[6] ] = Away( msg[6], msg[7], msg[8] )
            #print ("ES: AWAY - {0} Sz {1}".format( msg[6], len(self.uiES.Aways) ) )
    
        # Channel Link names and Status U (Up) D (Down)
        if  msg[ eMsgHdr.MsgType ] == 'L':
            self.uiES.Links[ msg[4] ] = CHLink( msg[6], msg[5] )
            Ch = self.uiES.Links[ msg[4] ]
            #print( "ES: Link {0} = {1} Sz {2}:({3},{4})".format( msg[4],  msg[6], len(self.uiES.Links), Ch.Stat, Ch.Type ) )
            # commented out - J

        # ETB List: to be kept for sending of Order.  Need to know Locate is required for symbols not on this list
        if  msg[ eMsgHdr.MsgType ] == 'F' and msg[ 4 ] == 'E':
            ct = 0
            for i in range(7, len(msg)-1 ):
                self.uiES.ETB.append(msg[i]) #appends to list per account in ETB List
                ct += 1
                #print("ETB has Symb {0}".format( msg[i] ) )
            #print ("ES: ETB has added {0} symbols.\n".format( ct ))

        # Max Shares and Value per Order.  Each order must NOT exceed this setting per Account
        if  msg[ eMsgHdr.MsgType ] == 'F' and msg[ 4 ] == 'X':
            for i in range(8, len(msg)-1):
                MxShSymbItms = msg[8].split(',')
                for s in range(0, len(MxShSymbItms)):
                    MxShrItms = MxShSymbItms[s].split('_')
                    if len(MxShrItms) == 3:
                        self.uiES.MaxShares[ msg[7] + '~' + MxShrItms[0] ] = MaxShrDollar( msg[7], MxShrItms[0], MxShrItms[1], MxShrItms[2])
                        #print('ES: MaxShrs Acct {0} Symb {1} has Shr Lmt per Order {2} and/or max order value {3}'.format( msg[7], MxShrItms[0], MxShrItms[1], MxShrItms[2]) )
                    
    def GetUserInfo(self):
        return self.uiES

    def GetAvailChan(self):
        UpLinks = 'UP LINKS:   '
        DnLinks = 'DOWN LINKS: '

        for i,l in self.uiES.Links.items():
            if l.Stat == 'U':
                UpLinks += i + ' '
            elif l.Stat == 'D':
                DnLinks += i + ' '
        print( UpLinks )
        print( DnLinks )

    def IsConnected(self):
        try:
            c_uint_p = POINTER(c_uint)
            rv = self.HAPI.dll.GetESConnState()
            if rv == 0: return 0
            return cast(rv, c_uint_p).contents.value
        except:
            return False
    
    def CheckForETBSymb(self,sSymb):
        return sSymb in self.uiES.ETB

    def CheckMaxValues(self, Acct, Symb, sQty, sPr):
        MxS = self.uiES.MaxShares.get( Acct + '~' + Symb )
        
        if  MxS != None:
            if  (int(MxS.MaxShr) > 0 and int(MxS.MaxShr) < int(sQty)) or \
                (float(MxS.MaxAmt) > 0 and float(MxS.MaxAmt) < (float(sQty)*float(sPr))):
                return False
        
        return True

    def GetLocQtyInSymb(self, Symb):
        Loc = self.uiES.Locates.get( Symb )
        if Loc != None:
            return Loc.nQtyAvail
        else:
            return None


 #    Traceback (most recent call last):
  # File "C:\Python27x86\lib\threading.py", line 801, in __bootstrap_inner
    # self.run()
  # File "C:\Python27x86\lib\threading.py", line 754, in run
    # self.__target(*self.__args, **self.__kwargs)
  # File "HAPIPY.py", line 385, in passive_thread
    # ES.SendCancelMsg(acct, passive_ticker, passive_buy_order_id, 'B') # later in the loop, rejoin the new best bid
  # File "E:\git\trading\zt\HAPIPY\EServerConnection.py", line 405, in SendCancelMsg
    # parent = orig_order.PNo
# AttributeError: 'NoneType' object has no attribute 'PNo'

    def SendCancelMsg(self, acct, ticker, order_id, side):

        # what does this first number mean, and the 069
        # #:02924:N:069:ABCD:0:1000058:C:MSFT:B:100:43.250::OUCH:DAY::L:ANY:Y:*

        if order_id == '': # simplify
            return
        
        #orig_order = self.uiES.Ords[acct][ticker][order_id]

        if side in ['B', 'BC']:
            key = 'buy'
        else:
            key = 'sell'
        orig_order = self.uiES.Ords[acct][ticker][key]
        if orig_order == None:
            return # concurrency workaround. not perfect


        parent = orig_order.PNo
        ticker = orig_order.Symb
        side = orig_order.Side
        size = orig_order.Qty
        px = orig_order.Pr
        chan = orig_order.Chan
        tif = orig_order.TIF
        o_type = orig_order.OType
        disp = orig_order.Disp

            
        # #:02924:N:069:ABCD:0:1000058:C:MSFT:B:100:43.250::OUCH:DAY::L:ANY:Y:*
        #:00000:N:000:DEMOX1:1:500022:C:NOK:B:100:1.0::DAY:L:::ANY:Y:*
        
        cancel_msg = "#:00000:N:000:{0}:{1}:{2}:C:{3}:{4}:{5}:{6}::{7}:{8}::{9}:ANY:{10}:*".format( \
                    acct, parent, order_id, ticker, side,
                    size, px, chan,
                    tif, o_type, disp).encode() # send original size, per david


        RVal = self.HAPI.dll.SendMsgES(cancel_msg)

        if self.print_on:
            print 'SENDING CANCEL: order {0} ({1} of {2} {3} @ {4})'.format(order_id, side, orig_order.nLvsQty, ticker, px)
        #print ("ES: Cancel={0} - {1}".format(RVal, cancel_msg))

    def SendETBReqMsg(self, acct):
        etb_msg = ':00000:F:000:E:0:0:{0}:*'.format(acct).encode()
        RVal = self.HAPI.dll.SendMsgES(etb_msg)
        if self.print_on:
            print 'SENDING ETB REQUEST'

    # ES: Send=83 - #:00000:N:000:DEMOX1:5::N:GDX:B:2866:22.59::CSFB:DAY::L::Y::100:::9,,,,,:8:GDX::::*

    # check cur buyign power before sending msg

    def SendESOrderMsg(self, sAcct='', sSymb='', sSd='', sQty='', sPr='', sContra='', sChan='', sTIF='', sOType='', sDisp ='', sCanRepID=''):
        if self.IsConnected() == 0:
            if self.previously_connected == True:
                if self.print_on:
                    print("ES: Connection is DOWN. trying to reconnect...")
                self.U_flag = False # assuming i get a U on reconnect
                self.ReconnectSvr()
            else:
                if self.print_on:
                    print 'ES: Connection NOT YET UP'
            return
        else:
            self.previously_connected = True

        if self.CheckMaxValues( sAcct, sSymb, sQty, sPr ) == False:
            if self.print_on:
                print("ES: Price and Quantity exceeds Max values set for this account for this symbol")
            return
        # Side if not BUY, determine if it will be long Sell or Short


        if sSd not in ['B', 'BC']:
            mpPos = self.uiES.OvPos.get(sAcct)
            if mpPos is None:
                sSd = 'T'
            else:
                Pos = mpPos.get(sSymb)
                if Pos is not None and Pos.Qty > int( sQty ):
                    sSd = 'S'
                else:
                    sSd = 'T'

        # if Short and HTB, chk for Available Locate Qty
        if sSd == 'T' and self.CheckForETBSymb( sSymb ) == False and sCanRepID == '': # only decrement locates if NOT a can/rep

            # the above check seems wrong
            # need to verify
            
            if self.uiES.Locates.get(sAcct) == None:
                Loc = None
            else:
                Loc = self.uiES.Locates[sAcct].get( sSymb ) # whole time, just wasn't indexing into acct first...



              # File "E:\git\trading\zt\HAPIPY\EServerConnection.py", line 453, in SendESOrderMsg
                # Loc = self.uiES.Locates[sAcct].get( sSymb ) # whole time, just wasn't indexing into acct first...
             #    KeyError: 'DEMOX1'

            if Loc != None:
                nLocQty = Loc.nQtyAvail
                if  nLocQty == None or (nLocQty != None and nLocQty < int(sQty)):
                    if self.print_on:
                        print("ES: Not Enough Located Qty {1} for SHORTING HTB Symb={0}".format( sSymb, nLocQty ) )
                    return
                else:
                    # deplete this qty from avail qty before sending out
                    self.uiES.Locates[sAcct][sSymb].UsedQty(int(sQty))

            else:
                if self.print_on:
                    print("ES: Not Enough Located Qty 0 for SHORTING HTB Symb={0}".format( sSymb ) )
                return

            
        sParent = ''
        sParent = str(self.getNextID())


        #:14418:N:000:ABCDEF:0:0:N:JOSB:T:500:59.12::GSAC:DAY::M::Y::300::0:3,15-59-52,16-00-00:8:JOSB::Q:USD:*
        #:00000:N:000:DEMOX1:1::N:NOK:B:100:1.0::CSFB:DAY::L::Y::100::::8:NOK::::*

        # NOTE: documentation is mislabeled for disp qty, as Max Floor Amt. use field 17 for display quantity
        # NOTE: for csfb PATHFINDER: use 9,,,,,
            # for csfb CROSSFINDER: use 4A,,,,,
        sOrderMsg = "#:00000:N:000:{0}:{1}::N:{2}:{3}:{4}:{5}:{6}:{7}:{8}::{9}::{10}::{12}:{11}::4A,,,,,:8:{2}::::*".format( \
                    sAcct, sParent, sSymb, sSd,
                    sQty, sPr, sContra, sChan,
                    sTIF, sOType, sDisp, sCanRepID, DEF_DISP_QTY).encode() # CanRepID required in cancel/replace orders. blank otherwise
        

        print(sOrderMsg)
        RVal    = self.HAPI.dll.SendMsgES(sOrderMsg)

        if self.print_on:
            print 'SENDING ORDER: {0} {1} {2} @ {3}'.format(sSd, sQty, sSymb, sPr)
        #print ("ES: Send={0} - {1}".format(RVal, sOrderMsg))

    def PrintPositionsList(self,sAcct='',sSymb=''):
        if self.print_on:
            print ('-------- Positions ----------')
        if sAcct == 'ALL' or sAcct == '':
            for k,sl in self.uiES.OvPos.items():
                for kk,l in sl.items():
                    if self.print_on:
                        print("ES: POS {0} {1} {2} {3} {4} {5}".format( l.Acct, l.Symb, l.Qty, l.Pr, l.LocInf.nQtyTot, l.LocInf.nQtyAvail ) )
            

        else:
            SymbList = self.uiES.OvPos.get( sAcct )

            if SymbList != None:
                if( sSymb ):
                    Pos = SymbList.get( sSymb )
                    if Pos != None:
                        if self.print_on:
                            print("ES: POS {0} {1} {2} {3} {4} {5}".format( sAcct, sSymb, Pos.Qty, Pos.Pr, Pos.LocInf.nQtyTot, Pos.LocInf.nQtyAvail ) )
                else:
                    for k,v in SymbList.items():
                        if self.print_on:
                            print ("ES: POS {0} {1} {2} {3} {4} {5}".format( v.Acct, v.Symb, v.Qty, v.Pr, v.LocInf.nQtyTot, v.LocInf.nQtyAvail ) )
            else:
                if self.print_on:
                    print('ES: Found no Positions with Account, {0}\n'.format( sAcct ) )


    def OnDisconnect(self):
        #self.uiES.OvPos.clear() # why would i clear these?
        #self.uiES.Locates.clear()
        self.session_start_timestamp = datetime.datetime.now()
        self.U_flag = False
        if self.print_on:
            print("ES: DISCONNECTED from ES.")

    def SetTrace(self, bTurnOn=True ):
        if bTurnOn == True:
            self.HAPI.dll.PostAdmMsgES(ADMMSG_TRACE_TOGGLE, 0, 7 )
        else:
            self.HAPI.dll.PostAdmMsgES(ADMMSG_TRACE_TOGGLE, 0, 0 )
    
    def ReconnectSvr(self):
        self.HAPI.dll.PostAdmMsgES(ADMMSG_RECONNECT, 0, 0 )

    def Exit(self):
        m = '#:25329:O:015:*'.encode()
        self.HAPI.dll.SendMsgES(m)
        time.sleep(1)
        self.HAPI.dll.HYDRAPIKITExit()
        #self.HAPI.dll.Exit()
        #self.HAPI.dll.HAPIKITExit()

        # print('sending logout message')
        # logout_message = '#:00000:O:015:*'
        #
        # self.HAPI.dll.SendMsgES(logout_message)
        # sleep(1)
        # ret = int()
        # print('calling EndSession')
        # self.HAPI.dll.EndSession(ret)
        # sleep(1)
        # return ret


    def SendHeartBeatMessage(self):
        """
        no need to send this, hapikit sends this, the returned T message shows connection
        :return:
        """
        self.HAPI.dll.SendMsgES('#:00000:H:000:*')

    def SendMessage(self, Msg):
        try:
            self.HAPI.dll.SendMsgES(Msg)
        except:
            print('Message submission failed.')



    def test2(self):
        """request level 1 data"""
        #:00000:1:000:SPY:A:*
        m = '#:00000:1:000:MSFT:A:*'
        ret = self.HAPI.dll.SendMsgES(m.encode())
        return ret

    def test3(self):
        """request level 1 data"""
        m = '#:00000:1:000:MSFT:R:*'
        ret = self.HAPI.dll.SendMsgES(m.encode())
        return ret