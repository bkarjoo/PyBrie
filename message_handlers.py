from message import *
from Quotes import *


class message_handlers:
    def __init__(self, quotes):
        self.quotes = quotes
        pass

    def es_a_handler(self, msg):
        print('a handler')
    def es_b_handler(self, msg):
        pass
    def es_c_handler(self, msg):
        pass
    def es_d_handler(self, msg):
        pass
    def es_e_handler(self, msg):
        pass
    def es_f_handler(self, msg):
        pass
    def es_g_handler(self, msg):
        pass
    def es_h_handler(self, msg):
        pass
    def es_i_handler(self, msg):
        pass
    def es_j_handler(self, msg):
        pass
    def es_k_handler(self, msg):
        pass
    def es_l_handler(self, msg):
        pass
    def es_m_handler(self, msg):
        pass
    def es_n_handler(self, msg):
        pass
    def es_o_handler(self, msg):
        pass
    def es_p_handler(self, msg):
        pass
    def es_q_handler(self, msg):
        pass
    def es_r_handler(self, msg):
        pass
    def es_s_handler(self, msg):
        pass
    def es_t_handler(self, msg):
        pass
    def es_u_handler(self, msg):
        pass
    def es_v_handler(self, msg):
        pass
    def es_w_handler(self, msg):
        pass
    def es_x_handler(self, msg):
        pass
    def es_y_handler(self, msg):
        pass
    def es_z_handler(self, msg):
        pass
    def is_1_handler(self, msg):
        self.quotes.update_1(msg.get_tokens())
    def is_2_handler(self, msg):
        pass
    def is_3_handler(self, msg):
        pass
    def is_4_handler(self, msg):
        pass
    def is_5_handler(self, msg):
        pass
    def is_6_handler(self, msg):
        pass
    def is_7_handler(self, msg):
        pass
    def is_8_handler(self, msg):
        pass
    def is_9_handler(self, msg):
        pass
    def is_0_handler(self, msg):
        pass
    def is_a_handler(self, msg):
        self.quotes.update_A(msg.get_tokens())
    def is_b_handler(self, msg):
        self.quotes.update_B(msg.get_tokens())
    def is_c_handler(self, msg):
        self.quotes.update_C(msg.get_tokens())
    def is_d_handler(self, msg):
        self.quotes.update_D(msg.get_tokens())
    def is_e_handler(self, msg):
        pass
    def is_f_handler(self, msg):
        self.quotes.update_F(msg.get_tokens())
    def is_g_handler(self, msg):
        self.quotes.update_G(msg.get_tokens())
    def is_h_handler(self, msg):
        self.quotes.update_H(msg.get_tokens())
    def is_i_handler(self, msg):
        pass
    def is_j_handler(self, msg):
        self.quotes.update_J(msg.get_tokens())
    def is_k_handler(self, msg):
        self.quotes.update_K(msg.get_tokens())
    def is_l_handler(self, msg):
        pass
    def is_m_handler(self, msg):
        pass
    def is_n_handler(self, msg):
        self.quotes.update_N(msg.get_tokens())
    def is_o_handler(self, msg):
        pass
    def is_p_handler(self, msg):
        pass
    def is_q_handler(self, msg):
        pass
    def is_r_handler(self, msg):
        pass
    def is_s_handler(self, msg):
        pass
    def is_t_handler(self, msg):
        pass
    def is_u_handler(self, msg):
        pass
    def is_v_handler(self, msg):
        self.quotes.update_V(msg.get_tokens())
    def is_w_handler(self, msg):
        pass
    def is_x_handler(self, msg):
        pass
    def is_y_handler(self, msg):
        pass
    def is_z_handler(self, msg):
        pass

    def es_message_handler(self, msg):
        msg_type = msg.get_message_type()
        cases = {
            'A': self.es_a_handler,
            'B': self.es_b_handler,
            'C': self.es_c_handler,
            'D': self.es_d_handler,
            'E': self.es_e_handler,
            'F': self.es_f_handler,
            'G': self.es_g_handler,
            'H': self.es_h_handler,
            'I': self.es_i_handler,
            'J': self.es_j_handler,
            'K': self.es_k_handler,
            'L': self.es_l_handler,
            'M': self.es_m_handler,
            'N': self.es_n_handler,
            'O': self.es_o_handler,
            'P': self.es_p_handler,
            'Q': self.es_q_handler,
            'R': self.es_r_handler,
            'S': self.es_s_handler,
            'T': self.es_t_handler,
            'U': self.es_u_handler,
            'V': self.es_v_handler,
            'W': self.es_w_handler,
            'X': self.es_x_handler,
            'Y': self.es_y_handler,
            'Z': self.es_z_handler
        }
        cases[msg_type](msg)

    def is_message_handler(self, msg):
        msg_type = msg.get_message_type()
        cases = {
            '1': self.is_1_handler,
            '2': self.is_2_handler,
            '3': self.is_3_handler,
            '4': self.is_4_handler,
            '5': self.is_5_handler,
            '6': self.is_6_handler,
            '7': self.is_7_handler,
            '8': self.is_8_handler,
            '9': self.is_9_handler,
            '0': self.is_0_handler,
            'A': self.is_a_handler,
            'B': self.is_b_handler,
            'C': self.is_c_handler,
            'D': self.is_d_handler,
            'E': self.is_e_handler,
            'F': self.is_f_handler,
            'G': self.is_g_handler,
            'H': self.is_h_handler,
            'I': self.is_i_handler,
            'J': self.is_j_handler,
            'K': self.is_k_handler,
            'L': self.is_l_handler,
            'M': self.is_m_handler,
            'N': self.is_n_handler,
            'O': self.is_o_handler,
            'P': self.is_p_handler,
            'Q': self.is_q_handler,
            'R': self.is_r_handler,
            'S': self.is_s_handler,
            'T': self.is_t_handler,
            'U': self.is_u_handler,
            'V': self.is_v_handler,
            'W': self.is_w_handler,
            'X': self.is_x_handler,
            'Y': self.is_y_handler,
            'Z': self.is_z_handler
        }
        cases[msg_type](msg)

    def handle_message(self, msg):
        if msg.get_message_server() == None:
            return
        elif msg.get_message_server() == message_server.is_server:
            self.is_message_handler(msg)
        elif msg.get_message_server() == message_server.es_server:
            self.es_message_handler(msg)


