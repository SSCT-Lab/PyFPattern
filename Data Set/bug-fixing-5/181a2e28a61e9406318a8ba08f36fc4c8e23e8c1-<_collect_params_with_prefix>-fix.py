def _collect_params_with_prefix(self, prefix=''):
    if prefix:
        prefix += '.'
    pattern = re.compile('(l|r)(\\d)_(i2h|h2h)_(weight|bias)\\Z')

    def convert_key(m, bidirectional):
        (d, l, g, t) = [m.group(i) for i in range(1, 5)]
        if bidirectional:
            return '_unfused.{}.{}_cell.{}_{}'.format(l, d, g, t)
        else:
            return '_unfused.{}.{}_{}'.format(l, g, t)
    bidirectional = any(((pattern.match(k).group(1) == 'r') for k in self._reg_params))
    ret = {(prefix + convert_key(pattern.match(key), bidirectional)): val for (key, val) in self._reg_params.items()}
    for (name, child) in self._children.items():
        ret.update(child._collect_params_with_prefix((prefix + name)))
    return ret