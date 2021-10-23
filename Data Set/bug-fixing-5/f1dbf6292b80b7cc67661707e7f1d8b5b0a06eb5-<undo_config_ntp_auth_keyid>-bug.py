def undo_config_ntp_auth_keyid(self):
    'Undo ntp authentication key-id'
    xml_str = (CE_NC_DELETE_NTP_AUTH_CONFIG % self.key_id)
    ret_xml = set_nc_config(self.module, xml_str)
    self.check_response(ret_xml, 'UNDO_NTP_AUTH_KEYID_CONFIG')