from order_status_fields import *

class submited_orders:
    """
    these are orders that are submited but not yet acknowledged
    order status would then acknowledge these and assigned order number generated by hydra
    """
    def __init__(self):
        self.orders = list()

    def add_order(self, o):
        self.orders.append(o)

    def find_order_by_status(self,os):
        """
        :return: the index of the order
        """
        for order in self.orders:
            if self.is_match(order,os):
                return self.orders.index(order)

        return -1

    def is_match(self, order, os):
        """
        if quantity symbol and price are equal assume match
        :param order: the order
        :param os: the status message tokenized
        :return: true if it's the same order
        """
        if order.quantity == os[OrderStatusFields.OSF_QUANTITY] \
            and order.symbol == os[OrderStatusFields.OSF_ORDER_SYMBOL] \
            and order.price == os[OrderStatusFields.OSF_ORDER_PRICE]:
            return True
        else:
            return False

    def remove_order_by_index(self, index):
        if index >= len(self.orders):
            return None
        return self.orders.pop(index)

    def order_count(self):
        return len(self.orders)