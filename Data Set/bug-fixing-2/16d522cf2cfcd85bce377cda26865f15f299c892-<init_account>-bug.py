

def init_account(self):
    '\n        Create or update an account on the ACME server. As the only way\n        (without knowing an account URI) to test if an account exists\n        is to try and create one with the provided account key, this\n        method will always result in an account being present (except\n        on error situations). If the account already exists, it will\n        update the contact information.\n        https://tools.ietf.org/html/draft-ietf-acme-acme-02#section-6.3\n        '
    contact = []
    if self.email:
        contact.append(('mailto:' + self.email))
    if (not self._new_reg(contact)):
        (result, _) = self.send_signed_request(self.uri, {
            'resource': 'reg',
        })
        if ('authorizations' in result):
            self._authz_list_uri = result['authorizations']
        if ('certificates' in result):
            self._certs_list_uri = result['certificates']
        do_update = False
        if ('contact' in result):
            if (cmp(contact, result['contact']) != 0):
                do_update = True
        elif (len(contact) > 0):
            do_update = True
        if do_update:
            upd_reg = result
            upd_reg['contact'] = contact
            (result, _) = self.send_signed_request(self.uri, upd_reg)
            self.changed = True
