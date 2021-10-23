def get_ntp_all_auth_keyid(self):
    'Get all authentication keyid info'
    ntp_auth_conf = list()
    flags = list()
    exp = ('| include authentication-keyid %s' % self.key_id)
    flags.append(exp)
    config = self.get_config(flags)
    ntp_config_list = config.split('\n')
    if (not ntp_config_list):
        self.ntp_auth_conf['authentication-keyid'] = 'None'
        return ntp_auth_conf
    self.key_id_exist = True
    cur_auth_mode = ''
    cur_auth_pwd = ''
    for ntp_config in ntp_config_list:
        ntp_auth_mode = re.findall('.*authentication-mode(\\s\\S*)\\s\\S*\\s(\\S*)', ntp_config)
        ntp_auth_trust = re.findall('.*trusted.*', ntp_config)
        if ntp_auth_trust:
            self.cur_trusted_key = 'enable'
        if ntp_auth_mode:
            cur_auth_mode = ntp_auth_mode[0][0].strip()
            cur_auth_pwd = ntp_auth_mode[0][1].strip()
    ntp_auth_conf.append(dict(key_id=self.key_id, auth_mode=cur_auth_mode, auth_pwd=cur_auth_pwd, trusted_key=self.cur_trusted_key))
    self.ntp_auth_conf['authentication-keyid'] = ntp_auth_conf
    return ntp_auth_conf