def setup(self, session=None):
    c_key = self.config['apikey'].get(unicode)
    c_secret = self.config['apisecret'].get(unicode)
    try:
        with open(self._tokenfile()) as f:
            tokendata = json.load(f)
    except IOError:
        (token, secret) = self.authenticate(c_key, c_secret)
    else:
        token = tokendata['token']
        secret = tokendata['secret']
    self.beatport_api = BeatportClient(c_key, c_secret, token, secret)