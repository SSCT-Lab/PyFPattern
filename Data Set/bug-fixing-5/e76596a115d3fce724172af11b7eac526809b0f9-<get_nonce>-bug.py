def get_nonce(self, resource=None):
    url = (self.directory_root if (self.version == 1) else self.directory['newNonce'])
    if (resource is not None):
        url = resource
    (dummy, info) = fetch_url(self.module, url, method='HEAD')
    if (info['status'] not in (200, 204)):
        raise ModuleFailException('Failed to get replay-nonce, got status {0}'.format(info['status']))
    return info['replay-nonce']