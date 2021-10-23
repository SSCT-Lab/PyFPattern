def __init__(self, *args, **kwargs):
    self._timeout = float(C.CACHE_PLUGIN_TIMEOUT)
    self._cache = {
        
    }
    self._cache_dir = os.path.expanduser(os.path.expandvars(C.CACHE_PLUGIN_CONNECTION))
    if (not self._cache_dir):
        raise AnsibleError('error, fact_caching_connection is not set, cannot use fact cache')
    if (not os.path.exists(self._cache_dir)):
        try:
            os.makedirs(self._cache_dir)
        except (OSError, IOError) as e:
            display.warning(('error while trying to create cache dir %s : %s' % (self._cache_dir, to_bytes(e))))
            return None