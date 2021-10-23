def merge_fragment(target, source):
    for (key, value) in source.items():
        if (key in target):
            if isinstance(target[key], MutableMapping):
                value.update(target[key])
            elif isinstance(target[key], MutableSet):
                value.add(target[key])
            elif isinstance(target[key], MutableSequence):
                value = sorted(frozenset((value + target[key])))
            else:
                raise Exception(('Attempt to extend a documentation fragement, invalid type for %s' % key))
            target[key] = value