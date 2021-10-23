def get(self, key):
    " This checks the in memory cache first as the fact was not expired at 'gather time'\n        and it would be problematic if the key did expire after some long running tasks and\n        user gets 'undefined' error in the same play "
    if (key in self._cache):
        return self._cache.get(key)
    if (self.has_expired(key) or (key == '')):
        raise KeyError
    cachefile = ('%s/%s' % (self._cache_dir, key))
    try:
        with codecs.open(cachefile, 'r', encoding='utf-8') as f:
            try:
                value = json.load(f)
                self._cache[key] = value
                return value
            except ValueError as e:
                display.warning(("error in 'jsonfile' cache plugin while trying to read %s : %s. Most likely a corrupt file, so erasing and failing." % (cachefile, to_bytes(e))))
                self.delete(key)
                raise AnsibleError(('The JSON cache file %s was corrupt, or did not otherwise contain valid JSON data. It has been removed, so you can re-run your command now.' % cachefile))
    except (OSError, IOError) as e:
        display.warning(("error in 'jsonfile' cache plugin while trying to read %s : %s" % (cachefile, to_bytes(e))))
        raise KeyError