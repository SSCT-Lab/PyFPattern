def send_signed_request(self, url, payload, key_data=None, jws_header=None, parse_json_result=True):
    '\n        Sends a JWS signed HTTP POST request to the ACME server and returns\n        the response as dictionary\n        https://tools.ietf.org/html/draft-ietf-acme-acme-14#section-6.2\n        '
    key_data = (key_data or self.key_data)
    jws_header = (jws_header or self.jws_header)
    failed_tries = 0
    while True:
        protected = copy.deepcopy(jws_header)
        protected['nonce'] = self.directory.get_nonce()
        if (self.version != 1):
            protected['url'] = url
        data = self.sign_request(protected, payload, key_data)
        if (self.version == 1):
            data['header'] = jws_header
        data = self.module.jsonify(data)
        headers = {
            'Content-Type': 'application/jose+json',
        }
        (resp, info) = fetch_url(self.module, url, data=data, headers=headers, method='POST')
        result = {
            
        }
        try:
            content = resp.read()
        except AttributeError:
            content = info.get('body')
        if (content or (not parse_json_result)):
            if ((parse_json_result and info['content-type'].startswith('application/json')) or (400 <= info['status'] < 600)):
                try:
                    decoded_result = self.module.from_json(content.decode('utf8'))
                    if ((400 <= info['status'] < 600) and (decoded_result.get('type') == 'urn:ietf:params:acme:error:badNonce') and (failed_tries <= 5)):
                        failed_tries += 1
                        continue
                    if parse_json_result:
                        result = decoded_result
                except ValueError:
                    raise ModuleFailException('Failed to parse the ACME response: {0} {1}'.format(url, content))
            else:
                result = content
        return (result, info)