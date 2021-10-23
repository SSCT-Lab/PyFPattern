

def run(self, priority, msg):
    ' Do, whatever it is, we do. '
    url = ('%s:%s/1/messages.json' % (self.base_uri, self.port))
    options = dict(user=self.user, token=self.token, priority=priority, message=msg)
    data = urllib.urlencode(options)
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
    }
    (r, info) = fetch_url(self.module, url, method='POST', data=data, headers=headers)
    if (info['status'] != 200):
        raise Exception(info)
    return r.read()
