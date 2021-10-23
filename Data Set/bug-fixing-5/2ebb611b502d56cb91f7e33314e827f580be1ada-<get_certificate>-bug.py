def get_certificate(self):
    '\n        Request a new certificate and write it to the destination file.\n        Only do this if a destination file was provided and if all authorizations\n        for the domains of the csr are valid. No Return value.\n        '
    if ((self.dest is None) and (self.fullchain_dest is None)):
        return
    if ((self.finalize_uri is None) and (self.version != 1)):
        return
    for domain in self.domains:
        auth = self.authorizations.get(domain)
        if ((auth is None) or ('status' not in auth) or (auth['status'] != 'valid')):
            return
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