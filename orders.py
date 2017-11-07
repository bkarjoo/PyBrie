from order import order

class orders:
    """
    a collection of order objects
    stores orders in a dictionary of orderId to order object
    orderIds are auto generated hhmmss00x
    this scheme alows for upto 1000 orders per second
    """

    def __init__(self):
        # key : parent_id
        # value : order object
        self.order_dict = {}

    def add_order(self, order):
        order_dict[id] = order
        return id




