def config_ntp_auth_keyid(self):
    'Config ntp authentication keyid'
    if (self.trusted_key == 'enable'):
        trusted_key = 'true'
    else:
        trusted_key = 'false'
    xml_str = (CE_NC_MERGE_NTP_AUTH_CONFIG % (self.key_id, self.auth_mode.upper(), self.password, trusted_key))
    ret_xml = set_nc_config(self.module, xml_str)
    self.check_response(ret_xml, 'NTP_AUTH_KEYID_CONFIG')