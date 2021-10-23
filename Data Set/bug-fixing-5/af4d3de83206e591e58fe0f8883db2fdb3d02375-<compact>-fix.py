def compact(seq):
    "\n    Removes ``None`` values from various sequence-based data structures.\n\n    dict:\n        Removes keys with a corresponding ``None`` value.\n\n    list:\n        Removes ``None`` values.\n\n    >>> compact({'foo': 'bar', 'baz': None})\n    {'foo': 'bar'}\n\n    >>> compact([1, None, 2])\n    [1, 2]\n    "
    if isinstance(seq, dict):
        return {k: v for (k, v) in six.iteritems(seq) if (v is not None)}
    elif isinstance(seq, list):
        return [k for k in seq if (k is not None)]