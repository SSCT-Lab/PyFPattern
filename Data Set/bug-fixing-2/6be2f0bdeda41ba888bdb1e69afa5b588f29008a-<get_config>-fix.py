

def get_config(self, config_format='text'):
    if (config_format not in SUPPORTED_CONFIG_FORMATS):
        self.raise_exc(msg=('invalid config format.  Valid options are %s' % ', '.join(SUPPORTED_CONFIG_FORMATS)))
    ele = self.rpc('get_configuration', output=config_format)
    if (config_format == 'text'):
        return unicode(ele.text).strip()
    else:
        return ele
