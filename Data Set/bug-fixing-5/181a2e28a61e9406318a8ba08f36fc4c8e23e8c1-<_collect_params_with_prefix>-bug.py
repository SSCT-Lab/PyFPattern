def _collect_params_with_prefix(self, prefix=''):
    if prefix:
        prefix += '.'

    def convert_key(key):
        key = key.split('_')
        return '_unfused.{}.{}_cell.{}'.format(key[0][1:], key[0][0], '_'.join(key[1:]))
    ret = {(prefix + convert_key(key)): val for (key, val) in self._reg_params.items()}
    for (name, child) in self._children.items():
        ret.update(child._collect_params_with_prefix((prefix + name)))
    return ret