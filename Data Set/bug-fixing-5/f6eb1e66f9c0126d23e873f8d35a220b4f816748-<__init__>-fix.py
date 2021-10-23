def __init__(self, *args, **kwargs):
    self.cache_fields = kwargs.pop('cache_fields', [])
    self.cache_ttl = kwargs.pop('cache_ttl', (60 * 5))
    self._cache_version = kwargs.pop('cache_version', None)
    self.__local_cache = threading.local()
    super(BaseManager, self).__init__(*args, **kwargs)