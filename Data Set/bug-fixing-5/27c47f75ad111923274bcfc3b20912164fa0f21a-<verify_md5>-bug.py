def verify_md5(self, file, remote_md5):
    result = False
    if os.path.exists(file):
        local_md5 = self._local_md5(file)
        remote = self._request(remote_md5, 'Failed to download MD5', (lambda r: r.read()))
        result = (local_md5 == remote)
    return result