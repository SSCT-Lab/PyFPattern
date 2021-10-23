def record_exists(self):
    update = dns.update.Update(self.zone, keyring=self.keyring, keyalgorithm=self.algorithm)
    try:
        update.present(self.module.params['record'], self.module.params['type'])
    except dns.rdatatype.UnknownRdatatype as e:
        self.module.fail_json(msg='Record error: {0}'.format(to_native(e)))
    response = self.__do_update(update)
    self.dns_rc = dns.message.Message.rcode(response)
    if (self.dns_rc == 0):
        if (self.module.params['state'] == 'absent'):
            return 1
        for entry in self.module.params['value']:
            try:
                update.present(self.module.params['record'], self.module.params['type'], entry)
            except AttributeError:
                self.module.fail_json(msg='value needed when state=present')
            except dns.exception.SyntaxError:
                self.module.fail_json(msg='Invalid/malformed value')
        response = self.__do_update(update)
        self.dns_rc = dns.message.Message.rcode(response)
        if (self.dns_rc == 0):
            if self.ttl_changed():
                return 2
            else:
                return 1
        else:
            return 2
    else:
        return 0