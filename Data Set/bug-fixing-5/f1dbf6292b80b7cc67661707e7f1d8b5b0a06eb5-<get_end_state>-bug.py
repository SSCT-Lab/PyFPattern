def get_end_state(self):
    'Get end state info'
    self.ntp_auth_conf = dict()
    self.get_ntp_auth_exist_config()
    self.end_state = copy.deepcopy(self.ntp_auth_conf)