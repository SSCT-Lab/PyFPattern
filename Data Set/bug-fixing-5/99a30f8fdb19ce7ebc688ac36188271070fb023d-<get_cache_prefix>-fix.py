def get_cache_prefix(self, path):
    ' create predictable unique prefix for plugin/inventory '
    m = hashlib.sha1()
    m.update(to_bytes(self.NAME))
    d1 = m.hexdigest()
    n = hashlib.sha1()
    n.update(to_bytes(path))
    d2 = n.hexdigest()
    return 's_'.join([d1[:5], d2[:5]])