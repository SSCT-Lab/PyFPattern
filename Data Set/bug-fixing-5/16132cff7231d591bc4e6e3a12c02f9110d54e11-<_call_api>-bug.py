def _call_api(self, path, video_id, note, data=None):
    base_url = ((self._API_DOMAIN + '/core/') + path)
    encoded_query = compat_urllib_parse_urlencode({
        'oauth_consumer_key': self._API_PARAMS['oAuthKey'],
        'oauth_nonce': ''.join([random.choice(string.ascii_letters) for _ in range(32)]),
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': int(time.time()),
        'oauth_version': '1.0',
    })
    headers = self.geo_verification_headers()
    if data:
        data = json.dumps(data).encode()
        headers['Content-Type'] = 'application/json'
    method = ('POST' if data else 'GET')
    base_string = '&'.join([method, compat_urlparse.quote(base_url, ''), compat_urlparse.quote(encoded_query, '')])
    oauth_signature = base64.b64encode(hmac.new((self._API_PARAMS['oAuthSecret'] + '&').encode('ascii'), base_string.encode(), hashlib.sha1).digest()).decode()
    encoded_query += ('&oauth_signature=' + compat_urlparse.quote(oauth_signature, ''))
    return self._download_json('?'.join([base_url, encoded_query]), video_id, note=('Downloading %s JSON metadata' % note), headers=headers, data=data)