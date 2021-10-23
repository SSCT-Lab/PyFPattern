def _validate_challenges(self, domain, auth):
    '\n        Validate the authorization provided in the auth dict. Returns True\n        when the validation was successful and False when it was not.\n        '
    for challenge in auth['challenges']:
        if (self.challenge != challenge['type']):
            continue
        uri = (challenge['uri'] if (self.version == 1) else challenge['url'])
        challenge_response = {
            
        }
        if (self.version == 1):
            token = re.sub('[^A-Za-z0-9_\\-]', '_', challenge['token'])
            keyauthorization = self.account.get_keyauthorization(token)
            challenge_response['resource'] = 'challenge'
            challenge_response['keyAuthorization'] = keyauthorization
        (result, info) = self.account.send_signed_request(uri, challenge_response)
        if (info['status'] not in [200, 202]):
            self.module.fail_json(msg='Error validating challenge: CODE: {0} RESULT: {1}'.format(info['status'], result))
    status = ''
    while (status not in ['valid', 'invalid', 'revoked']):
        result = simple_get(self.module, auth['uri'])
        result['uri'] = auth['uri']
        if self._add_or_update_auth(domain, result):
            self.changed = True
        if ((self.version == 1) and ('status' not in result)):
            status = 'pending'
        else:
            status = result['status']
        time.sleep(2)
    if (status == 'invalid'):
        self._fail_challenge(domain, result, 'Authorization for {0} returned invalid')
    return (status == 'valid')