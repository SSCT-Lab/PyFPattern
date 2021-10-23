

def get_certificate(self):
    '\n        Request a new certificate and write it to the destination file.\n        First verifies whether all authorizations are valid; if not, aborts\n        with an error.\n        '
    for (identifier_type, identifier) in self.identifiers:
        auth = self.authorizations.get(((identifier_type + ':') + identifier))
        if (auth is None):
            raise ModuleFailException('Found no authorization information for "{0}"!'.format(((identifier_type + ':') + identifier)))
        if ('status' not in auth):
            self._fail_challenge(identifier_type, identifier, auth, 'Authorization for {0} returned no status')
        if (auth['status'] != 'valid'):
            self._fail_challenge(identifier_type, identifier, auth, ('Authorization for {0} returned status ' + str(auth['status'])))
    if (self.version == 1):
        cert = self._new_cert_v1()
    else:
        cert_uri = self._finalize_cert()
        cert = self._download_cert(cert_uri)
        if self.module.params['retrieve_all_alternates']:
            alternate_chains = []
            for alternate in cert['alternates']:
                try:
                    alt_cert = self._download_cert(alternate)
                except ModuleFailException as e:
                    self.module.warn('Error while downloading alternative certificate {0}: {1}'.format(alternate, e))
                    continue
                alternate_chains.append(alt_cert)
            self.all_chains = []

            def _append_all_chains(cert_data):
                self.all_chains.append(dict(cert=cert_data['cert'].encode('utf8'), chain='\n'.join(cert_data.get('chain', [])).encode('utf8'), full_chain=(cert_data['cert'] + '\n'.join(cert_data.get('chain', []))).encode('utf8')))
            _append_all_chains(cert)
            for alt_chain in alternate_chains:
                _append_all_chains(alt_chain)
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
