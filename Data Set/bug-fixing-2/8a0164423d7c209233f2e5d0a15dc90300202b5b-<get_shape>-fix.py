

def get_shape(self, key):
    "\n        get shape of the parameter.\n\n        :param key: parameter name\n        :type key: basestring\n        :return: parameter's shape\n        :rtype: tuple\n        "
    if (not isinstance(key, basestring)):
        raise ValueError('parameter name should be string')
    if (not self.has_key(key)):
        raise ValueError(('No such parameter %s' % key))
    conf = self.__param_conf__[key]
    dims = (conf.dims if conf.dims else (1, conf.size))
    return tuple(map(int, dims))
