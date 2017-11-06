import time
import datetime
from order import order

class orders:
    """
    a collection of order objects
    stores orders in a dictionary of orderId to order object
    orderIds are auto generated hhmmss00x
    this scheme alows for upto 1000 orders per second
    """

    def __init__(self):
        self.order_number = 0
        self.time_stamp = '{:%H%M%S}'.format(datetime.datetime.now())
        # key : parent_id
        # value : order object
        self.order_dict = {}

    def generate_order_id(self):
        """
        :return:order id string
        """
        current_time_stamp = '{:%H%M%S}'.format(datetime.datetime.now())
        if current_time_stamp != self.time_stamp:
            self.order_number = 0
            self.time_stamp = current_time_stamp
        else:
            self.order_number += 1
        if self.order_number < 10:
            ord_num_str = '00' + str(self.order_number)
        elif self.order_number < 100:
            ord_num_str = '0' + str(self.order_number)
        else:
            ord_num_str = str(self.order_number)
        time.sleep(.1)
        return '{:%H%M%S}'.format(datetime.datetime.now()) + ord_num_str

    def add_order(self, order):
        id = ords.generate_order_id()
        order_dict[id] = order
        return id

ords = orders()

for x in range(0,1000):
    print(ords.generate_order_id())


