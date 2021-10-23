def _fqdn_name(self, value):
    if value.startswith('/'):
        name = os.path.basename(value)
        result = '/{0}/{1}'.format(self.partition, name)
    else:
        result = '/{0}/{1}'.format(self.partition, value)
    return result