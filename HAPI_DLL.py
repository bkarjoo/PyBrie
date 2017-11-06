from ctypes import *
from _ctypes import FreeLibrary
from time import *
import threading
from EServerConnection import EServerConnection
from IServerConnection import IServerConnection

ES = EServerConnection()
IS = IServerConnection()
class HAPI_DLL:
    def __init__    (self, dll, SI):
        self.dll    = windll.LoadLibrary(dll)
        self.si     = SI
        global ES
        global IS
        ES.setHAPI(self)
        IS.setHAPI(self)

    def __del__     (self):
        FreeLibrary( self.dll._handle )

    def GrabSession(self):
        #thread HoldSession_Until_Termination
        try:
            nRet    = self.dll.HYDRAPIKITSession2( byref(self.si) )
            print('Exited with RetVal %d' % nRet)
        except:
            print ('Exception caught during HYDRAPIKITSession2() call...\n')
        del self

    def Run(self):
        self.hThread = threading.Thread( target=self.GrabSession, name="HoldSession_Until_Termination" )
        self.hThread.start()


