

def local_cmp(a, b):
    '\n        compares with only values and not keys, keys should be the same for both dicts\n        :param a: dict 1\n        :param b: dict 2\n        :return: difference of values in both dicts\n        '
    diff = [key for key in a if (a[key] != b[key])]
    return len(diff)
