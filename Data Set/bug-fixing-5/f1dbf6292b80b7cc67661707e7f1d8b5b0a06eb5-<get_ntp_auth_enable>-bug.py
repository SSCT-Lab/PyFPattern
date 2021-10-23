def get_ntp_auth_enable(self):
    'Get ntp authentication enable state'
    xml_str = CE_NC_GET_NTP_AUTH_ENABLE
    con_obj = get_nc_config(self.module, xml_str)
    if ('<data/>' in con_obj):
        return
    auth_en = re.findall('.*<isAuthEnable>(.*)</isAuthEnable>.*', con_obj)
    if auth_en:
        if (auth_en[0] == 'true'):
            self.ntp_auth_conf['authentication'] = 'enable'
        else:
            self.ntp_auth_conf['authentication'] = 'disable'