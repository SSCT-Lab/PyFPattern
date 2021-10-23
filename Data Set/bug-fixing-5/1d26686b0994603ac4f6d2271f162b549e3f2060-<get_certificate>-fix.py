def get_certificate(self):
    '\n        Request a new certificate and write it to the destination file.\n        Only do this if a destination file was provided and if all authorizations\n        for the domains of the csr are valid. No Return value.\n        '
    if (self.dest is None):
        return
    for domain in self.domains:
        auth = self._get_domain_auth(domain)
        if ((auth is None) or ('status' not in auth) or (auth['status'] != 'valid')):
            return
    cert = self._new_cert()
    if (cert['cert'] is not None):
        pem_cert = self._der_to_pem(cert['cert'])
        chain = [self._der_to_pem(link) for link in cert.get('chain', [])]
        if (chain and self.module.params['fullchain']):
            pem_cert += '\n'.join(chain)
        if write_file(self.module, self.dest, pem_cert):
            self.cert_days = get_cert_days(self.module, self.dest)
            self.changed = True