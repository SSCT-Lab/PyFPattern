def is_invalid_md5(self, file, remote_url):
    if os.path.exists(file):
        local_md5 = self._local_md5(file)
        if self.local:
            parsed_url = urlparse(remote_url)
            remote_md5 = self._local_md5(parsed_url.path)
        else:
            remote_md5 = self._getContent((remote_url + '.md5'), 'Failed to retrieve MD5', False)
            if (not remote_md5):
                return ('Cannot find md5 from ' + remote_url)
        if (local_md5 == remote_md5):
            return None
        else:
            return ((('Checksum does not match: we computed ' + local_md5) + 'but the repository states ') + remote_md5)
    return ('Path does not exist: ' + file)