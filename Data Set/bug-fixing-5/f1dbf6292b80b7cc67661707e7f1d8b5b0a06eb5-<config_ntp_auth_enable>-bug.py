def config_ntp_auth_enable(self):
    'Config ntp authentication enable'
    if (self.ntp_auth_conf['authentication'] != self.authentication):
        if (self.authentication == 'enable'):
            state = 'true'
        else:
            state = 'false'
        xml_str = (CE_NC_MERGE_NTP_AUTH_ENABLE % state)
        ret_xml = set_nc_config(self.module, xml_str)
        self.check_response(ret_xml, 'NTP_AUTH_ENABLE')