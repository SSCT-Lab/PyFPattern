def has_expired(self, key):
    if (self._timeout == 0):
        return False
    cachefile = ('%s/%s' % (self._cache_dir, key))
    try:
        st = os.stat(cachefile)
    except (OSError, IOError) as e:
        if (e.errno == errno.ENOENT):
            return False
        else:
            display.warning(('error while trying to stat %s : %s' % (cachefile, to_bytes(e))))
            pass
    if ((time.time() - st.st_mtime) <= self._timeout):
        return False
    if (key in self._cache):
        del self._cache[key]
    return True