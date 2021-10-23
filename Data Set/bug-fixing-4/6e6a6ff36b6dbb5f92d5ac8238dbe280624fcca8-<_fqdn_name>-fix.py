def _fqdn_name(self, value):
    if ((value is not None) and (not value.startswith('/'))):
        return '/{0}/{1}'.format(self.partition, value)
    return value