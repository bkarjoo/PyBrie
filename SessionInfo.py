from ctypes import *

class HySessionInfo(Structure):
    _fields_ = [
                ( "Login",      c_char * 32 ),
                ( "Password",   c_char * 32 ),
                ( "IP",         c_char * 32 ),
                ( "Port",       c_int ) 
                ]

class SessionInfo(Structure):
    fnMsgHdlr_t   = CFUNCTYPE( None, c_char_p )
    fnCleanUp_t   = CFUNCTYPE( None )
    _fields_ = [
                ( "HydraSessionInfo",   c_voidp ),
                ( "ESMsgHdlr",          fnMsgHdlr_t ),
                ( "ISMsgHdlr",          fnMsgHdlr_t ),
                ( "ESCleanUp",          fnCleanUp_t ),
                ( "ISCleanUp",          fnCleanUp_t )
                ]
