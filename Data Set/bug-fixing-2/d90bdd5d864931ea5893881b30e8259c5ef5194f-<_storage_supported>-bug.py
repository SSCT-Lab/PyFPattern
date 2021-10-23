

def _storage_supported(self, uri):
    scheme = urlparse(uri).scheme
    if (scheme in self.storages):
        try:
            self._get_storage(uri)
            return True
        except NotConfigured:
            logger.error('Disabled feed storage scheme: %(scheme)s', {
                'scheme': scheme,
            })
    else:
        logger.error('Unknown feed storage scheme: %(scheme)s', {
            'scheme': scheme,
        })
