from enum import Enum
from collections import *

class eMsgHdr(Enum):
    MsgStart    = 0
    Token       = 1
    MsgType     = 2
    MsgLen      = 3
class eMsgAcct(Enum):
    ID          = 4
    BP          = 5
    RBP         = 6
    ATyp        = 7
    FirmID      = 8
class eMsgONPos(Enum):
    ACCT        = 4
    SYMB        = 5
    SIDE        = 6
    ONQTY       = 7
    ONPR        = 8


class Accounts:
    def __init__(self, ID, BP, RBP, AType, FirmID):
        self.ID         = ID
        self.BP         = BP
        self.RBP        = RBP
        self.AType      = AType
        self.FirmID     = FirmID

class LocateInfo:
    nQtyAvail = 0
    nQtyTot = 0
    def __init__(self, nQty=0 ):
        self.AddedQty(nQty)

    def AddedQty( self, Qty=0 ):
        self.nQtyAvail += Qty
        self.nQtyTot += Qty

    def IsAvailable( self, Qty=0 ):
        if self.nQtyAvail > Qty:
            return True
        else:
            return False
    def UsedQty( self, Qty=0 ):
        # OK to be negative
        self.nQtyAvail -= Qty 
            
    def Buying( self, Qty=0 ):
        self.nQtyAvail += Qty
        if self.nQtyTot < self.nQtyAvail:
            self.nQtyAvail = self.nQtyTot


class Position:
    Acct    = ''
    Symb    = ''
    Qty     = 0
    Pr      = 0.0
    LocInf  = LocateInfo()

    def __init__(self, sAcct, sSymb, nQty, nPr, LocInfo = LocateInfo() ):
        self.Acct   = sAcct
        self.Symb   = sSymb
        self.Qty    = nQty
        self.Pr     = nPr
        self.LocInf = LocInfo


# seems like this is pointless. cut out
class ODetails:
    Ord = None
    def __init__(self,  TmSt='', Acct='', OrdID='', Sub='',
                        Qty='', Pr='', Cntra='', Chan='',
                        Stat='', Txt='', LvsQty='' ):
        self.TmSt   = TmSt
        self.Acct   = Acct
        self.OrdID  = OrdID
        self.Sub    = Sub
        self.Qty    = Qty
        self.Pr     = Pr
        self.Cntra  = Cntra
        self.Chan   = Chan
        self.Stat   = Stat
        self.Txt    = Txt
        self.LvsQty = LvsQty

class Order:
    nCumQty    = 0
    nAvgPr     = 0.0
    nLvsQty    = 0
    #Det        = ''
    PNo        = ''
    TmSt       = ''
    Acct       = ''
    OrdID      = ''
    Symb       = ''
    Side       = ''
    Qty        = ''
    Pr         = ''
    OType      = ''
    Cntra      = ''
    Chan       = ''
    TIF        = ''
    MinQty     = ''
    Disp       = ''
    PegType    = ''
    PegOff     = ''
    DiscOff    = ''
    MaxFl      = ''
    TickID     = ''
    AlgoDet    = ''
    OrgSide    = ''
    

    def __init__(self,  #Det={'': ODetails},
                        PNo='', TmSt='', Acct='', OrdID='',
                        Symb='', Side='', Qty='', Pr='', 
                        Cntra='', Chan='', TIF='', OType='', 
                        MinQty='', Disp='', PegType='', PegOff='', 
                        DiscOff='', MaxFl='', TickID='', AlgoDet='', 
                        OrgSide=''):
        #self.Det        = Det
        self.PNo        = PNo
        self.TmSt       = TmSt
        self.Acct       = Acct
        self.OrdID      = OrdID
        self.Symb       = Symb
        self.Side       = Side
        self.Qty        = Qty
        self.Pr         = Pr
        self.OType      = OType
        self.Cntra      = Cntra
        self.Chan       = Chan
        self.TIF        = TIF
        self.MinQty     = MinQty
        self.Disp       = Disp
        self.PegType    = PegType 
        self.PegOff     = PegOff
        self.DiscOff    = DiscOff
        self.MaxFl      = MaxFl
        self.TickID     = TickID
        self.AlgoDet    = AlgoDet
        self.OrgSide    = OrgSide
        self.nLvsQty    = int( Qty )

    
    def UpdateNewOrder( self,
                        PNo='', TmSt='', Acct='', OrdID='',
                        Symb='', Side='', Qty='', Pr='', 
                        OType='', Cntra='', Chan='', TIF='', 
                        MinQty='', Disp='', PegType='', PegOff='', 
                        DiscOff='', MaxFl='', TickID='', AlgoDet='', 
                        OrgSide=''):
        self.PNo        = PNo
        self.TmSt       = TmSt
        self.Acct       = Acct
        self.OrdID      = OrdID
        self.Symb       = Symb
        self.Side       = Side
        self.Qty        = Qty
        self.Pr         = Pr
        self.OType      = OType
        self.Cntra      = Cntra
        self.Chan       = Chan
        self.TIF        = TIF
        self.MinQty     = MinQty
        self.Disp       = Disp
        self.PegType    = PegType 
        self.PegOff     = PegOff
        self.DiscOff    = DiscOff
        self.MaxFl      = MaxFl
        self.TickID     = TickID
        self.AlgoDet    = AlgoDet
        self.OrgSide    = OrgSide
        self.nLvsQty    = int( Qty )


    
    def AddExecution( self, nLstQty, nLstPr ):
        if (self.nCumQty + nLstQty) != 0:
            self.nAvgPr     = ( self.nCumQty * self.nAvgPr + nLstQty * nLstPr)/(self.nCumQty + nLstQty)
        else:
            self.nAvgPr     = 0.0
        self.nCumQty    += nLstQty
        self.nLvsQty    -= nLstQty


    

class Away:
    def __init__(self, MPID='', Info='', FirmID=''):
        self.MPID   = MPID
        self.Info   = Info
        self.FirmID = FirmID

class CHLink:
    Stat    = ''
    Type    = ''
    def __init__(self, Stat='', Type=''):
        self.Stat   = Stat
        self.Type   = Type

class MaxShrDollar:
    def __init__(self, Acct='', Symb='', MaxShr='', MaxAmt=''):
        self.Acct   = Acct
        self.Symb   = Symb
        self.MaxShr = MaxShr
        self.MaxAmt = MaxAmt


class UserInfo:
    Accts       ={}
    OvPos       ={'': { '': Position } } # Account key, Symbol 2nd key
    #Ords        ={'': {'': { '': Order }} } # Account, ticker, OrderID

    Ords  = {'': {'': { 'buy': Order, 'sell': Order }} }
    # what about a dict of lists

    Aways       ={'': Away}
    Links       ={'': CHLink}
    ETB         =[]
    MaxShares   ={'': MaxShrDollar}
    Locates     ={'': {'':LocateInfo} }

