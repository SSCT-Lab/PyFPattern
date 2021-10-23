def get_ntp_auth_enable(self):
    'Get ntp authentication enable state'
    flags = list()
    exp = '| exclude undo | include ntp authentication'
    flags.append(exp)
    config = self.get_config(flags)
    auth_en = re.findall('.*ntp\\s*authentication\\s*enable.*', config)
    if auth_en:
        self.ntp_auth_conf['authentication'] = 'enable'
    else:
        self.ntp_auth_conf['authentication'] = 'disable'