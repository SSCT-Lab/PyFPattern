def get_certificate(self):
    '\n        Request a new certificate and write it to the destination file.\n        First verifies whether all authorizations are valid; if not, aborts\n        with an error.\n        '
    for domain in self.domains:
        auth = self.authorizations.get(domain)
        if (auth is None):
            self.module.fail_json(msg='Found no authorization information for "{0}"!'.format(domain))
        if ('status' not in auth):
            self._fail_challenge(domain, auth, 'Authorization for {0} returned no status')
        if (auth['status'] != 'valid'):
            self._fail_challenge(domain, auth, ('Authorization for {0} returned status ' + str(auth['status'])))
    if (self.version == 1):
        cert = self._new_cert_v1()
    else:
        cert_uri = self._finalize_cert()
        cert = self._download_cert(cert_uri)
    if (cert['cert'] is not None):
        pem_cert = cert['cert']
        chain = [link for link in cert.get('chain', [])]
        if (self.dest and write_file(self.module, self.dest, pem_cert.encode('utf8'))):
            self.cert_days = get_cert_days(self.module, self.dest)
            self.changed = True
        if (self.fullchain_dest and write_file(self.module, self.fullchain_dest, (pem_cert + '\n'.join(chain)).encode('utf8'))):
            self.cert_days = get_cert_days(self.module, self.fullchain_dest)
            self.changed = True
        if (self.chain_dest and write_file(self.module, self.chain_dest, '\n'.join(chain).encode('utf8'))):
            self.changed = True