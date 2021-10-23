def send_signed_request(self, url, payload):
    '\n        Sends a JWS signed HTTP POST request to the ACME server and returns\n        the response as dictionary\n        https://tools.ietf.org/html/draft-ietf-acme-acme-02#section-5.2\n        '
    protected = copy.deepcopy(self.jws_header)
    protected['nonce'] = self.directory.get_nonce()
    try:
        payload64 = nopad_b64(self.module.jsonify(payload).encode('utf8'))
        protected64 = nopad_b64(self.module.jsonify(protected).encode('utf8'))
    except Exception as e:
        self.module.fail_json(msg='Failed to encode payload / headers as JSON: {0}'.format(e))
    openssl_sign_cmd = [self._openssl_bin, 'dgst', '-sha256', '-sign', self.key]
    sign_payload = '{0}.{1}'.format(protected64, payload64).encode('utf8')
    (_, out, _) = self.module.run_command(openssl_sign_cmd, data=sign_payload, check_rc=True, binary_data=True)
    data = self.module.jsonify({
        'header': self.jws_header,
        'protected': protected64,
        'payload': payload64,
        'signature': nopad_b64(to_bytes(out)),
    })
    (resp, info) = fetch_url(self.module, url, data=data, method='POST')
    result = {
        
    }
    try:
        content = resp.read()
    except AttributeError:
        content = info.get('body')
    if content:
        if info['content-type'].startswith('application/json'):
            try:
                result = self.module.from_json(content.decode('utf8'))
            except ValueError:
                self.module.fail_json(msg='Failed to parse the ACME response: {0} {1}'.format(url, content))
        else:
            result = content
    return (result, info)