def fetch_key(self, url):
    'Downloads a key from url, returns a valid path to a gpg key'
    (rsp, info) = fetch_url(self.module, url)
    if (info['status'] != 200):
        self.module.fail_json(msg=('failed to fetch key at %s , error was: %s' % (url, info['msg'])))
    key = rsp.read()
    if (not is_pubkey(key)):
        self.module.fail_json(msg=('Not a public key: %s' % url))
    (tmpfd, tmpname) = tempfile.mkstemp()
    tmpfile = os.fdopen(tmpfd, 'w+b')
    tmpfile.write(key)
    tmpfile.close()
    return tmpname