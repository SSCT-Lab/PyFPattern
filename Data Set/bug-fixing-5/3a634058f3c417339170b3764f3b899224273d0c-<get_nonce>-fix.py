def get_nonce(self, resource=None):
    url = self.directory_root
    if (resource is not None):
        url = resource
    (_, info) = fetch_url(self.module, url, method='HEAD')
    if (info['status'] != 200):
        self.module.fail_json(msg='Failed to get replay-nonce, got status {0}'.format(info['status']))
    return info['replay-nonce']