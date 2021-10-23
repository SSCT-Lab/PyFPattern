

def _storage_supported(self, uri):
    scheme = urlparse(uri).scheme
    if (scheme in self.storages):
        try:
            self._get_storage(uri)
            return True
        except NotConfigured as e:
            logger.error('Disabled feed storage scheme: %(scheme)s. Reason: %(reason)s', {
                'scheme': scheme,
                'reason': str(e),
            })
    else:
        logger.error('Unknown feed storage scheme: %(scheme)s', {
            'scheme': scheme,
        })
