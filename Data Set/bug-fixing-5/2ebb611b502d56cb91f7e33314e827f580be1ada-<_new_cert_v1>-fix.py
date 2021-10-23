def _new_cert_v1(self):
    '\n        Create a new certificate based on the CSR (ACME v1 protocol).\n        Return the certificate object as dict\n        https://tools.ietf.org/html/draft-ietf-acme-acme-02#section-6.5\n        '
    openssl_csr_cmd = [self._openssl_bin, 'req', '-in', self.csr, '-outform', 'DER']
    (dummy, out, dummy) = self.module.run_command(openssl_csr_cmd, check_rc=True)
    new_cert = {
        'resource': 'new-cert',
        'csr': nopad_b64(to_bytes(out)),
    }
    (result, info) = self.account.send_signed_request(self.directory['new-cert'], new_cert)
    chain = []
    if ('link' in info):
        link = info['link']
        parsed_link = re.match('<(.+)>;rel="(\\w+)"', link)
        if (parsed_link and (parsed_link.group(2) == 'up')):
            chain_link = parsed_link.group(1)
            (chain_result, chain_info) = fetch_url(self.module, chain_link, method='GET')
            if (chain_info['status'] in [200, 201]):
                chain = [self._der_to_pem(chain_result.read())]
    if (info['status'] not in [200, 201]):
        self.module.fail_json(msg='Error new cert: CODE: {0} RESULT: {1}'.format(info['status'], result))
    else:
        return {
            'cert': self._der_to_pem(result),
            'uri': info['location'],
            'chain': chain,
        }