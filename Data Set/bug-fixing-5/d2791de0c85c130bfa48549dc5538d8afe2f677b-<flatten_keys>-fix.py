def flatten_keys(self, items):
    '\n        Returns a normalized set of keys based on the various formats accepted\n        by TSDB methods. The input is either just a plain list of keys for the\n        top level or a `{level1_key: [level2_key, ...]}` dictionary->list map.\n        '
    if isinstance(items, (list, tuple)):
        return (items, None)
    elif isinstance(items, dict):
        return (items.keys(), list(set.union(*(set(v) for v in items.values()))))
    else:
        return (None, None)