from string_builder import StringBuilder
from SessionInfo import *
from EServerConnection import *
from IServerConnection import *
from HAPI_DLL import *
from UserInfo import *
from order import *
from message import *
from messages import *
from message_handlers import *
from quote import *
from Quotes import *

global HAPI
global acct
global HSI
global ES
global IS
global session_setv

global is_ready
global quit


def ESMsgHdlr(Msg):
    try:
        # now = datetime.datetime.now()
        # print(str(now))
        # print(Msg)
        m = es_message(Msg)
        global is_ready
        if m.get_message_type() == 'U':
            is_ready = True
            print('\nIS READY\n\nBriePy>>>')
        elif m.get_message_type() == 'Z':
            print(m.msg)
        global es_message_list
        global es_message_archive
        global archiving
        global message_handler
        if archiving:
            # es_message_archive.append(m)
            global i
            i = i + 1
            if m.get_message_type() == 'U':
                archiving = False

        else:
            es_message_list.append(m)
            message_handler.handle_message(m)

        ES.HandleESMsg(m.msg)
    except:
        try:
            print(MSG)
            print('ERROR in call back')
        except:
            pass

def ISMsgHdlr(Msg):
    # now = datetime.datetime.now()
    # print(str(now))
    # print(Msg)
    m = is_message(Msg)
    # global is_message_list
    # is_message_list.append(m)
    IS.HandleISMsg(m.msg)
    global message_handler
    message_handler.handle_message(m)

def CleanUpES():
    ES.OnDisconnect()

def CleanUpIS():
    pass

def get_menu():
    sb = StringBuilder()
    sb.Append("\nmenu\t\t\t-- prints this menu")
    sb.Append("\nquit\t\t\t-- quits the program")
    sb.Append("\nset_session\t\t-- setup new session")
    sb.Append("\nalgo\t\t\t-- automatically connect to algogroup")
    sb.Append("\ndemo\t\t\t-- automatically connect to demo account")
    sb.Append("\nes_status\t\t-- connection status of the execution server")
    sb.Append("\nis_status\t\t-- connection status of the information server")
    sb.Append("\n")
    sb.Append("\n---- ES Commands ----")
    sb.Append("\nes_message_count\t\t-- number of messages received from execution server")
    sb.Append("\nprint_es_messages\t\t-- prints all messages received in ES")
    sb.Append("\nprint_es_archive\t\t-- print all messages in archive")
    sb.Append("\nprint_es_filter\t\t\t-- prints only messages of specified type")
    sb.Append("\nprint_es_archive_filter\t-- print only messages of specified type")
    sb.Append("\nprint_es_types\t\t\t-- prints all types encountered in list.")
    sb.Append("\nprint_es_archive_types\t-- prints all types encountered in list.")
    sb.Append("\nbuy 100 XYZ 23.50 day\t-- submit buy order, side qty symb price tif")
    sb.Append("\nsell 100 XYZ 23.50 day\t-- submit buy order, side qty symb price tif")
    sb.Append("\nbc 100 XYZ 23.50 day\t-- submit buy order, side qty symb price tif")
    sb.Append("\nsh 100 XYZ 23.50 day\t-- submit buy order, side qty symb price tif")
    sb.Append("\n")
    sb.Append("\n---- IS Commands ----")
    sb.Append("\nis_message_count\t-- number of messages received from information server")
    sb.Append("\nprint_is_messages\t-- prints all messages received in IS")
    sb.Append("\nprint_is_filter\t\t-- prints only messages of specified type")
    sb.Append("\nprint_is_types\t\t-- prints all message which have printed.")
    sb.Append("\nquote\t\t\t\t-- prints a quote.")

    # subscribe
    # get current quote for subscribed to symbol
    sb.Append("\n")
    return sb

def get_char(inp = 'Enter a char', choice_filter = []):
    while True:
        i = raw_input(inp)
        if len(i) > 1:
            print('Please enter a single character', choice_filter)
            continue
        if len(choice_filter) == 0 and i != '':
            return i
        if i != '':
            for c in choice_filter:
                if i == c:
                    return i
        if len(choice_filter) == 0:
            print('Please enter a character.')
        else:
            print('Please enter: ', choice_filter)

def run():
    global es_message_archive
    global es_message_list
    global is_message_list
    global archiving
    global is_message_handler
    global message_handler
    global quotes
    global acct
    quotes = Quotes()
    message_handler = message_handlers(quotes)
    """archive messages until you encounter the U message"""
    archiving = True
    es_message_archive = messages('ES')
    es_message_list = messages('ES')
    is_message_list = messages('IS')
    session_set = False
    while True:
        command = raw_input("BriePy>>")

        if command == 'quit' or command == 'q':
            if session_set:
                ES.Exit()
            global quit
            quit = True
            break

        if command == 'menu' or command == 'm':
            print(get_menu())

        if command == 'set_session' or command == 'ss':
            choice = 0
            print("1. algogroup")
            print("2. demo")
            choice = get_char('Enter 1 or 2 (c to cancel):',['1','2','c'])
            if choice == '1' or choice == 1:
                HSI = HySessionInfo(b"algogroup", b"algogroup", b"10.17.240.155", 8701)
                acct = 'ALGOPAIR'

                ESHdlr = SessionInfo.fnMsgHdlr_t(ESMsgHdlr)
                ISHdlr = SessionInfo.fnMsgHdlr_t(ISMsgHdlr)
                ESClUp = SessionInfo.fnCleanUp_t(CleanUpES)
                ISClUp = SessionInfo.fnCleanUp_t(CleanUpIS)

                SI = SessionInfo(addressof(HSI), ESHdlr, ISHdlr, ESClUp, ISClUp)
                HAPI = HAPI_DLL(".\\HAPIKIT.DLL", SI)
                HAPI.Run()
                ES.set_print_on(False)
                sleep(2)
                session_set = True
            elif choice == '2' or choice == 2:
                HSI = HySessionInfo(b"demo", b"demo", b"10.17.240.159", 7620)
                acct = 'DEMOX1'

                ESHdlr = SessionInfo.fnMsgHdlr_t(ESMsgHdlr)
                ISHdlr = SessionInfo.fnMsgHdlr_t(ISMsgHdlr)
                ESClUp = SessionInfo.fnCleanUp_t(CleanUpES)
                ISClUp = SessionInfo.fnCleanUp_t(CleanUpIS)

                SI = SessionInfo(addressof(HSI), ESHdlr, ISHdlr, ESClUp, ISClUp)
                HAPI = HAPI_DLL(".\\HAPIKIT.DLL", SI)
                HAPI.Run()
                ES.set_print_on(False)
                sleep(2)
                session_set = True

        if command == 'es_status' or command == 'es':

            if ES.IsConnected():
                print("ES is connected.")
            else:
                print("ES is not connected.")

        if command == 'is_status' or command == 'is':

            if IS.IsConnected():
                print("IS is connected.")
            else:
                print("IS is not connected.")

        if command == 'algo' or command == 'a':
            HSI = HySessionInfo(b"algogroup", b"algogroup", b"10.17.240.155", 8701)
            acct = 'ALGOPAIR'
            ESHdlr = SessionInfo.fnMsgHdlr_t(ESMsgHdlr)
            ISHdlr = SessionInfo.fnMsgHdlr_t(ISMsgHdlr)
            ESClUp = SessionInfo.fnCleanUp_t(CleanUpES)
            ISClUp = SessionInfo.fnCleanUp_t(CleanUpIS)

            SI = SessionInfo(addressof(HSI), ESHdlr, ISHdlr, ESClUp, ISClUp)
            HAPI = HAPI_DLL(".\\HAPIKIT.DLL", SI)
            HAPI.Run()
            ES.set_print_on(False)

            sleep(2)
            session_set = True

        if command == 'demo' or command == 'd':
            HSI = HySessionInfo(b"demo", b"demo", b"10.17.240.159", 7620)
            acct = 'DEMOX1'

            ESHdlr = SessionInfo.fnMsgHdlr_t(ESMsgHdlr)
            ISHdlr = SessionInfo.fnMsgHdlr_t(ISMsgHdlr)
            ESClUp = SessionInfo.fnCleanUp_t(CleanUpES)
            ISClUp = SessionInfo.fnCleanUp_t(CleanUpIS)

            SI = SessionInfo(addressof(HSI), ESHdlr, ISHdlr, ESClUp, ISClUp)
            HAPI = HAPI_DLL(".\\HAPIKIT.DLL", SI)
            HAPI.Run()
            ES.set_print_on(False)
            sleep(2)
            session_set = True

        if command == 'is_message_count' or command == 'imc':
            print('IS Message Count', is_message_list.message_count())

        if command == 'es_message_count' or command == 'emc':
            print('ES Message Count', es_message_list.message_count())
            print('ES Archive Count', es_message_archive.message_count())

        if command == 'print_es_messages' or command == 'pem':
            es_message_list.print_message_list()

        if command == 'print_es_archive' or command == 'pea':
            es_message_archive.print_message_list()

        if command == 'print_is_messages' or command == 'pim':
            is_message_list.print_message_list()

        if command == 'print_is_filter' or command == 'pif':
            message_type = get_char('Enter message type>>>')
            is_message_list.print_message_list(message_type)

        if command == 'print_es_filter' or command == 'pef':
            message_type = get_char('Enter message type>>>')
            es_message_list.print_message_list(message_type)

        if command == 'print_es_archive_filter' or command == 'peaf':
            message_type = get_char('Enter message type>>>')
            es_message_archive.print_message_list(message_type)

        if command == 'print_es_types' or command == 'pet':
            es_message_list.print_types()

        if command == 'print_es_archive_types' or command == 'peat':
            es_message_archive.print_types()

        if command == 'print_is_types' or command == 'pit':
            is_message_list.print_types()

        if command[:4] == 'sell':
            """sell 100 XYZ 23.50 day ALGOPAIR"""
            """sell 100 XYZ 23.50 loo ALGOSYND"""
            """sell 100 XYZ moo ALGOGROUP"""
            """sell 100 XYZ vwap 23.5 stop ALGOSYND"""
            """sell 100 XYZ vwap 23.5 * 0.99 stop ALGOGROUP"""
            values = command.split(' ')
            qty = int(values[1])
            # -qty means sell
            qty = qty * -1
            o = order()
            acct = 'ALGOGROUP'
            if values[3].upper() == 'MOO':
                if len(values) == 5:
                    acct = values[4]
                o = generate_opg_market_order(qty, value[2], values[4])
            elif values[4].upper() =='LOO':
                if len(values) == 6:
                    acct = values[5]
                o = generate_limit_order(qty, value[2], value[3], values[5])
            elif values[4].upper() == 'DAY':
                if len(values) == 6:
                    acct = values[5]
                o = generate_limit_order(qty, values[2], values[3], values[5])
            elif values[4].upper() == 'STOP':
                if len(values) == 8:
                    acct = values[7]
                o = generate_stop_limit_order(qty, values[2], values[3], values[5], acct)
            elif values[3].upper() == 'VWAP':
                if values[5] == '*':
                    price = float(values[4])
                    multiplier = float(values[6])
                    price = round(price * multiplier, 2)
                    if len(values) == 9:
                        acct = values[8]
                    o = generate_nite_vwap_order(qty, values[2], '09-45-00', '13-00-00', price, acct)
                else:
                    if len(values) == 7:
                        acct = values[6]
                    o = generate_nite_vwap_order(qty, values[2], '09-45-00', '13-00-00', values[4], acct)

            o.submit()


        if command[:3] == 'buy':
            """buy 100 XYZ 23.50 day (ALGOPAI)"""
            """buy 100 XYZ 23.50 loo (ALGOSYND)"""
            """buy 100 XYZ moo (ALGOGROUP)"""
            """buy 100 XYZ 23.5 stop 23.75 limit (ALGOGROUP)"""
            """buy 100 XYZ VWAP 23.5 stop (ALGOGROUP)"""
            """buy 100 XYZ VWAP 23.5 * 1.01 stop (ALGOGROUP)"""
            values = command.split(' ')
            o = order()
            acct = 'ALGOGROUP'
            if values[3].upper() == 'MOO':
                if len(values) == 5:
                    acct = values[4]
                o = generate_opg_market_order(values[1],values[2],acct)
            elif values[4].upper() == 'LOO':
                if len(values) == 6:
                    acct = values[5]
                o = generate_limit_order(values[1],values[2],values[3],acct)
            elif values[4].upper() == 'DAY':
                if len(values) == 6:
                    acct = values[5]
                o = generate_limit_order(values[1],values[2],values[3],acct)
            elif values[4].upper() == 'STOP':
                if len(values) == 8:
                    acct = values[7]
                o = generate_stop_limit_order(values[1],values[2],values[3],values[5],acct)
            elif values[3].upper() == 'VWAP':
                if values[5] == '*':
                    price = float(values[4])
                    multiplier = float(values[6])
                    price = round(price * multiplier,2)
                    if len(values) == 9:
                        acct = values[8]
                    o = generate_nite_vwap_order(values[1], values[2], '09-45-00', '13-00-00', price, acct)
                else:
                    if len(values) == 7:
                        acct = values[6]
                    o = generate_nite_vwap_order(values[1], values[2], '09-45-00', '13-00-00', values[4], acct)

            o.submit()


        if command[:7] == 'buy loo':
            # send loo order
            # buy loo 100 XYZ 999.99
            values = command.split(' ')
            o = order()
            o.account = acct
            o.parrent_id = '0' # should be autogenerated by orders.

            pass

        if command[:2] == 'bc':
            """buy 100 XYZ 23.50 day"""
            values = command.split(' ')

            o = order()
            o.account = acct
            o.parrent_id = '0'
            o.order_id = '0'
            o.operation = operation_type.new_order
            o.symbol = values[2]
            o.side = side_type.buy_to_cover
            o.quantity = values[1]
            o.order_price = values[3]
            o.channel_of_execution = 'CSFB'
            if values[4] == 'day':
                o.tif = tif_type.day
            else:
                o.tif = tif_type.day
            o.type = order_type.limit
            o.display = display_mode.lit
            o.reserve_size = 300
            o.ticket_id = '0'
            o.algo_type = '3'
            o.algo_start_time = '15-59-52'
            o.algo_end_time = '16-00-00'
            ES.SendESOrderMsg(sAcct=o.account, sSymb=o.symbol, sSd=o.side, sQty=o.quantity,
                              sPr=o.order_price, sContra='', sChan=o.channel_of_execution,
                              sTIF=o.tif, sOType=o.type, sDisp='Y')

        if command[:2] == 'sh':
            """sh 100 XYZ 23.50 day"""
            values = command.split(' ')

            o = order()
            o.account = acct
            o.parrent_id = '0'
            o.order_id = '0'
            o.operation = operation_type.new_order
            o.symbol = values[2]
            o.side = side_type.short
            o.quantity = values[1]
            o.order_price = values[3]
            o.channel_of_execution = 'CSFB'
            if values[4] == 'day':
                o.tif = tif_type.day
            else:
                o.tif = tif_type.day
            o.type = order_type.limit
            o.display = display_mode.lit
            o.reserve_size = 300
            o.ticket_id = '0'
            o.algo_type = '3'
            o.algo_start_time = '15-59-52'
            o.algo_end_time = '16-00-00'
            ES.SendESOrderMsg(sAcct=o.account, sSymb=o.symbol, sSd=o.side, sQty=o.quantity,
                              sPr=o.order_price, sContra='', sChan=o.channel_of_execution,
                              sTIF=o.tif, sOType=o.type, sDisp='Y')

        if command == 'test':
            o = order()
            o.account = acct
            o.parrent_id = '0'
            o.order_id = '0'
            o.operation = operation_type.new_order
            o.symbol = 'NOK'
            o.side = side_type.buy
            o.quantity = 100
            o.order_price = 4.85
            o.channel_of_execution = 'CSFB'
            o.tif = tif_type.day
            o.type = order_type.limit
            o.display = display_mode.lit
            o.reserve_size = 300
            o.ticket_id = '0'
            o.algo_type = '3'
            o.algo_start_time = '15-59-52'
            o.algo_end_time = '16-00-00'
            ES.SendESOrderMsg(sAcct=o.account, sSymb=o.symbol, sSd=o.side, sQty=o.quantity,
                              sPr=o.order_price, sContra='', sChan=o.channel_of_execution,
                              sTIF=o.tif, sOType=o.type, sDisp='Y')

        if command == 'test2':
            ret = ES.test2()
            print ret

        if command == 'test3':
            ret = ES.test3()
            print ret

        if command == 'test4':
            IS.AddRemDataSub('SPY','A','1')

        if command == 'test5':

            msg = "#:00000:1:000:{0}:{1}:*".format('SPY', 'A')

            RVal = HAPI.dll.SendMsgIS(msg.encode())
            print ("IS: Subscribe={0} - {1}".format(RVal, msg))

        if command == 'test6':
            try:
                o = order()
                o.account = acct
                i = raw_input('enter parrent id: ')
                o.parrent_id = i
                o.order_id = '0'
                o.operation = operation_type.new_order
                i = raw_input('enter symbol: ')
                o.symbol = i
                o.side = side_type.buy
                i = raw_input('enter qty: ')
                o.quantity = int(i)
                i = raw_input('enter price: ')
                o.order_price = round(float(i),2)
                i = raw_input('enter channel')
                o.channel_of_execution = i
                o.tif = tif_type.day

                i = raw_input('enter type L M:')
                o.type = i
                o.display = display_mode.lit
                o.reserve_size = 300
                ES.SendESOrderMsg(sAcct=o.account, sSymb=o.symbol, sSd=o.side, sQty=o.quantity,
                                  sPr=o.order_price, sContra='', sChan=o.channel_of_execution,
                                  sTIF=o.tif, sOType=o.type, sDisp='Y')
            except:
                print('Order entry failed!')

        if command == 'quote':
            symb = raw_input("Enter symbol:")
            print(quotes.get_quote(symb))

        if command == 'submit':
            msg = raw_input("enter message:")
            ES.SendMessage(msg)


def heartbeat_loop():
    global i
    i = 0
    t = threading.Thread(target=run)
    t.start()
    global is_ready
    is_ready = False
    global quit
    quit = False
    while (True):
        if is_ready:
            ES.SendHeartBeatMessage()
        elif (not ES.IsConnected()):
            print(i)
            print('\nES is not connected!\nBriePy>>>')
        if (quit):
            break
        sleep(5)


if __name__ == "__main__":
    heartbeat_loop()
    print('DONE')