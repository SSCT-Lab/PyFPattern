

def is_invalid_md5(self, file, remote_url):
    if os.path.exists(file):
        local_md5 = self._local_md5(file)
        if self.local:
            parsed_url = urlparse(remote_url)
            remote_md5 = self._local_md5(parsed_url.path)
        else:
            try:
                remote_md5 = to_text(self._getContent((remote_url + '.md5'), 'Failed to retrieve MD5', False), errors='strict')
            except UnicodeError as e:
                return ('Cannot retrieve a valid md5 from %s: %s' % (remote_url, to_native(e)))
            if (not remote_md5):
                return ('Cannot find md5 from ' + remote_url)
        try:
            _remote_md5 = remote_md5.split(None)[0]
            remote_md5 = _remote_md5
        except IndexError as e:
            pass
        if (local_md5 == remote_md5):
            return None
        else:
            return ((('Checksum does not match: we computed ' + local_md5) + 'but the repository states ') + remote_md5)
    return ('Path does not exist: ' + file)
