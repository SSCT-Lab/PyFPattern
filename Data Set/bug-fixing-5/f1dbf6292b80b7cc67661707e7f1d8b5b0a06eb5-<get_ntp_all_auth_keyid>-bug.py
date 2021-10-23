def get_ntp_all_auth_keyid(self):
    'Get all authentication keyid info'
    ntp_auth_conf = list()
    xml_str = CE_NC_GET_ALL_NTP_AUTH_CONFIG
    con_obj = get_nc_config(self.module, xml_str)
    if ('<data/>' in con_obj):
        self.ntp_auth_conf['authentication-keyid'] = 'None'
        return ntp_auth_conf
    ntp_auth = re.findall('.*<keyId>(.*)</keyId>.*\\s*<mode>(.*)</mode>.*\\s*<keyVal>(.*)</keyVal>.*\\s*<isReliable>(.*)</isReliable>.*', con_obj)
    for ntp_auth_num in ntp_auth:
        if (ntp_auth_num[0] == self.key_id):
            self.key_id_exist = True
            if (ntp_auth_num[3] == 'true'):
                self.cur_trusted_key = 'enable'
            else:
                self.cur_trusted_key = 'disable'
        if (ntp_auth_num[3] == 'true'):
            trusted_key = 'enable'
        else:
            trusted_key = 'disable'
        ntp_auth_conf.append(dict(key_id=ntp_auth_num[0], auth_mode=ntp_auth_num[1].lower(), trusted_key=trusted_key))
    self.ntp_auth_conf['authentication-keyid'] = ntp_auth_conf
    return ntp_auth_conf