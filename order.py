class tif_type:
    day = 'DAY'
    ioc = 'IOC'
class operation_type:
    new_order = 'N'
    htb_new_order = 'M'
    cancel = 'C'
    none = None
class side_type:
    buy = 'B'
    sell = 'S'
    short = 'T'
    buy_to_cover = 'BC'
    none = None
class channel:
    CSFB = 'CSFB'
    NITE = 'NITE'
class order_type:
    limit = 'L'
    market = 'M'
class display_mode:
    hidden = 'N'
    lit = 'Y'
class algo_types:
    twap = '5'
    vwap = '6'

class order:
    """
    represents an order with all its fields
    """


    def __init__(self):
        self.account = ''
        self.parrent_id = ''
        self.order_id = ''
        self.operation = operation_type.none
        self.symbol = ''
        self.side = side_type.none
        self.quantity = 0
        self.order_price = 0.0
        self.contra = ''
        self.channel_of_execution = channel.CSFB
        self.tif = tif_type.day
        self.type = order_type.market
        self.display = display_mode.lit
        self.exec_price = ''
        self.reserve_size = ''
        self.cancel_replace_id = ''
        self.ticket_id = 0
        self.algo_type = ''
        self.algo_start_time = ''
        self.algo_end_time = ''

    def __str__(self):
        return "#:00000:N:000:{0}:{1}:{2}:N:{3}:{4}:{5}:{6}:{7}:{8}:{9}::{10}::{11}::{13}:{12}:{14}:{15},{16},{17}:::*".format(
            self.account, self.parrent_id, self.order_id, self.symbol, self.side,
            self.quantity, self.order_price, self.contra, self.channel_of_execution,
            self.tif, self.type, self.display, self.cancel_replace_id,
            self.reserve_size, self.ticket_id, self.algo_type, self.algo_start_time,
            self.algo_end_time)

    def submit(self):
        # use ES SendESOrderMsg
        # order submits itself
        #       easier implementation
        #       potential for double submit
        #       submission results saved within order
        # order submitter sumbits orders
        #       batch processing easier
        #       results can be used to organize orders into group
        #

        pass