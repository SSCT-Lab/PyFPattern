def send_signed_request(self, url, payload):
    '\n        Sends a JWS signed HTTP POST request to the ACME server and returns\n        the response as dictionary\n        https://tools.ietf.org/html/draft-ietf-acme-acme-09#section-6.2\n        '
    failed_tries = 0
    while True:
        protected = copy.deepcopy(self.jws_header)
        protected['nonce'] = self.directory.get_nonce()
        if (self.version != 1):
            protected['url'] = url
        try:
            payload64 = nopad_b64(self.module.jsonify(payload).encode('utf8'))
            protected64 = nopad_b64(self.module.jsonify(protected).encode('utf8'))
        except Exception as e:
            raise ModuleFailException('Failed to encode payload / headers as JSON: {0}'.format(e))
        openssl_sign_cmd = [self._openssl_bin, 'dgst', '-{0}'.format(self.key_data['hash']), '-sign', self.key]
        sign_payload = '{0}.{1}'.format(protected64, payload64).encode('utf8')
        (dummy, out, dummy) = self.module.run_command(openssl_sign_cmd, data=sign_payload, check_rc=True, binary_data=True)
        if (self.key_data['type'] == 'ec'):
            (dummy, der_out, dummy) = self.module.run_command([self._openssl_bin, 'asn1parse', '-inform', 'DER'], data=out, binary_data=True)
            expected_len = (2 * self.key_data['point_size'])
            sig = re.findall(('prim:\\s+INTEGER\\s+:([0-9A-F]{1,%s})\\n' % expected_len), to_text(der_out, errors='surrogate_or_strict'))
            if (len(sig) != 2):
                raise ModuleFailException('failed to generate Elliptic Curve signature; cannot parse DER output: {0}'.format(to_text(der_out, errors='surrogate_or_strict')))
            sig[0] = (((expected_len - len(sig[0])) * '0') + sig[0])
            sig[1] = (((expected_len - len(sig[1])) * '0') + sig[1])
            out = (binascii.unhexlify(sig[0]) + binascii.unhexlify(sig[1]))
        data = {
            'protected': protected64,
            'payload': payload64,
            'signature': nopad_b64(to_bytes(out)),
        }
        if (self.version == 1):
            data['header'] = self.jws_header
        data = self.module.jsonify(data)
        (resp, info) = fetch_url(self.module, url, data=data, method='POST')
        result = {
            
        }
        try:
            content = resp.read()
        except AttributeError:
            content = info.get('body')
        if content:
            if (info['content-type'].startswith('application/json') or (400 <= info['status'] < 600)):
                try:
                    result = self.module.from_json(content.decode('utf8'))
                    if ((400 <= info['status'] < 600) and (result.get('type') == 'urn:ietf:params:acme:error:badNonce') and (failed_tries <= 5)):
                        failed_tries += 1
                        continue
                except ValueError:
                    raise ModuleFailException('Failed to parse the ACME response: {0} {1}'.format(url, content))
            else:
                result = content
        return (result, info)