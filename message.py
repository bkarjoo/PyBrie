class message_server:
    is_server = 0
    es_server = 1


class es_message_field:
    type = 2
    length = 3
    # A : account details message
    a_account = 4
    a_bp_ini = 5
    a_bp_cur = 6
    # B : override account message
    b_override_account_id = 4
    b_channel_list = 5
    # B : Broadcast order flow msg (has more fields than override account msg)
    b_side = 4
    b_symbol = 5
    b_order_price = 6
    b_channel = 7
    b_contra_mm = 8
    b_qty = 9
    b_order_status = 10
    b_broadcast_account = 11
    b_order_id = 12
    # C : customer account message
    c_customer_account_id = 4
    c_text_description = 5
    # D : away mpid list message
    d_message_index_no = 4
    d_maximum_number_of_msgs = 5
    d_mpid = 6
    d_company_info = 7
    d_firm_id = 8
    # E : Firm Channel List Message
    e_firm_id = 4
    e_channel_list = 5
    # F Threshold (T) or ETB (E) Request Msg
    f_flag = 4
    # F T and E flags
    f_msg_index_1 = 5
    f_msg_index_2 = 6
    f_firm_id = 7
    # TODO : not f_message field 8 - x are each T or ETB symbols
    # F S flag : Account Sell Mode
    f_s_attached_acct_count = 5
    f_s_account_id = 6
    f_s_sell_mode = 7
    f_s_buying_power_mode = 8
    # F X flag : Symbol Max Shares Per Account
    f_x_index_counter = 5
    f_x_max_counter = 6
    f_X_account_id = 7
    f_x_symb_qty_exp_vals = 8
    # F M Flag Account Restriction / Max Dollar-Share per Order Messag
    f_m_attached_acct_count = 5
    f_m_reserved = 6
    f_m_account_id = 7
    f_m_max_dollar_amount = 8
    f_m_max_size = 9
    f_m_stop_loss = 10
    f_m_override_stop_loss = 11
    # G : Cancel Replace Order Request
    g_account = 4
    g_reserve1 = 5  # reserved
    g_reserve2 = 6  # reserved
    g_cr_message = 7
    g_symbol = 8
    g_side = 9
    g_size = 10
    g_price = 11
    g_contra_mmid = 12
    g_channel = 13
    g_tif = 14
    g_reserve3 = 15
    g_order_type = 16
    g_min_qty = 17
    g_display_Y_N = 18
    g_execution_instructions = 19
    g_max_floor = 20
    g_original_order_id = 21
    g_ticket_id = 22
    g_algo_details = 23
    # I : login response message
    i_overnite_count = 4
    i_new_order_count = 5
    i_order_status_msg_count = 6
    i_new_order_plus_stat_msg_count = 7
    i_es_version_number = 8
    # M : combine locate and new order/can/replace message

    # N : Order Request Message / cancel request
    n_account_id = 4
    n_parrent_no = 5
    n_order_id = 6
    n_operation = 7  # C for cancel
    n_symbol = 8
    n_side = 9
    n_qty = 10
    n_order_price = 11
    n_contra_mm = 12
    n_channel = 13
    n_tif = 14
    n_expiry_date = 15
    n_order_type = 16
    n_minimum_qty = 17
    n_display_mode = 18
    n_execution_instruction = 19
    n_max_floor_amount = 20
    n_cancel_replace_id = 21
    n_ticket_id = 22
    n_algo_details = 23
    n_security_type = 24
    n_security_id = 25
    # P : overnight open position message
    p_account_id = 4
    p_symbol = 5
    p_status = 6
    p_qty = 7
    p_avg_price = 8
    # S : Order Details Message (New Order/Order Status
    s_detail_type = 4
    s_report_type = 5
    s_f_parrent_no = 6
    s_f_date_time = 7
    s_f_account_id = 8
    s_f_order_id = 9
    s_f_symbol = 10
    s_f_side = 11
    s_f_quantity = 12
    s_f_order_price = 13
    s_f_contra = 14
    s_f_channel = 15
    s_f_tif = 16
    s_f_expiry = 17
    s_f_order_type = 18
    s_f_min_qty = 19
    s_f_display_Y_N = 20
    s_f_peg_type = 21
    s_f_pef_offset = 22
    s_f_discretionary_offset = 23
    s_f_max_floor_show_size = 24
    s_f_ticket_id = 25
    s_f_algo = 26
    s_f_original_side = 27
    s_s_date_time = 6
    s_s_account_id = 7
    s_s_order_id = 8
    s_s_order_sub_id = 9  # partials
    s_s_qty = 10
    s_s_order_price = 11
    s_s_contra = 12
    s_s_channel = 13
    s_s_status = 14
    s_s_error_status = 15  # error message for status R (reject)
    s_s_symbol = 16
    s_s_side = 17
    s_s_order_type = 18
    s_s_ticker_id = 19
    s_s_leaves_qty = 20
    # U : login end message
    u_message_index_no = 4
    u_maximum_number_of_msgs = 5
    u_mpid = 6
    u_company_info = 7
    u_firm_id = 8
    # W : Ticket Messages:

    # Z : Error Message
    z_error_text = 4


class message(object):
    def __init__(self, a_message):
        self.msg = a_message.decode('utf-8')
        self.tokens = self.msg.split(':')
        self.msg_server = None

    def get_message_type(self):
        if len(self.tokens) >= 3:
            return self.tokens[2]
        else:
            return None

    def get_message_server(self):
        return self.msg_server

    def __str__(self):
        return self.msg

    def get_tokens(self):
        return self.tokens

    def get_field(self, field):
        try:
            return self.tokens[field]
        except:
            return None

class is_message(message):
    def __init__(self, a_message):
        super(is_message, self).__init__(a_message)
        self.msg_server = message_server.is_server


class es_message(message):
    def __init__(self, a_message):
        super(es_message, self).__init__(a_message)
        self.msg_server = message_server.es_server


