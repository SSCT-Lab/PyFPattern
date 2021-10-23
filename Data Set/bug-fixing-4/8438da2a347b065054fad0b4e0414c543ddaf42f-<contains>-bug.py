def contains(self, key):
    cachefile = ('%s/%s' % (self._cache_dir, key))
    if (key in self._cache):
        return True
    if self.has_expired(key):
        return False
    try:
        os.stat(cachefile)
        return True
    except (OSError, IOError) as e:
        if (e.errno == errno.ENOENT):
            return False
        else:
            display.warning(('error while trying to stat %s : %s' % (cachefile, to_bytes(e))))
            pass