def _get_challenge_data(self, auth, domain):
    '\n        Returns a dict with the data for all proposed (and supported) challenges\n        of the given authorization.\n        '
    data = {
        
    }
    for challenge in auth['challenges']:
        type = challenge['type']
        token = re.sub('[^A-Za-z0-9_\\-]', '_', challenge['token'])
        keyauthorization = self.account.get_keyauthorization(token)
        if (type == 'http-01'):
            resource = ('.well-known/acme-challenge/' + token)
            data[type] = {
                'resource': resource,
                'resource_value': keyauthorization,
            }
        elif (type == 'tls-sni-02'):
            token_digest = hashlib.sha256(token.encode('utf8')).hexdigest()
            ka_digest = hashlib.sha256(keyauthorization.encode('utf8')).hexdigest()
            len_token_digest = len(token_digest)
            len_ka_digest = len(ka_digest)
            resource = 'subjectAlternativeNames'
            value = ['{0}.{1}.token.acme.invalid'.format(token_digest[:(len_token_digest // 2)], token_digest[(len_token_digest // 2):]), '{0}.{1}.ka.acme.invalid'.format(ka_digest[:(len_ka_digest // 2)], ka_digest[(len_ka_digest // 2):])]
            data[type] = {
                'resource': resource,
                'resource_value': value,
            }
        elif (type == 'dns-01'):
            resource = '_acme-challenge'
            value = nopad_b64(hashlib.sha256(to_bytes(keyauthorization)).digest())
            record = ((resource + domain[1:]) if domain.startswith('*.') else ((resource + '.') + domain))
            data[type] = {
                'resource': resource,
                'resource_value': value,
                'record': record,
            }
        else:
            continue
    return data