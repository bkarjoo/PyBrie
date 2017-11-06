from message_types import *

class messages:

    def __init__(self, server):
        self.msg_list = []
        self.types = set()
        self.server = server

    def append(self, msg):
        self.msg_list.append(msg)
        self.types.add(msg.get_message_type())

    def print_message_list(self, filter = ''):
        if filter == '':
            for msg in self.msg_list:
                print msg
        else:
            for msg in self.msg_list:
                if msg.get_message_type() == filter:
                    print msg

    def message_count(self):
        return len(self.msg_list)

    def print_types(self):
        print(self.types)
        for type in self.types:
            if self.server == 'ES':
                desc = message_types.es_types[type]
            elif self.server == 'IS':
                desc = message_types.is_types[type]
            print(type, desc)

    def get_server(self):
        return self.server