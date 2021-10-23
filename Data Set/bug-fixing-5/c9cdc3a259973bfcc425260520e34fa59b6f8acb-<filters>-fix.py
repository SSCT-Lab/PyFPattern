def filters(self):
    filters = {
        'min': min,
        'max': max,
        'log': logarithm,
        'pow': power,
        'root': inversepower,
        'unique': unique,
        'intersect': intersect,
        'difference': difference,
        'symmetric_difference': symmetric_difference,
        'union': union,
        'permutations': itertools.permutations,
        'combinations': itertools.combinations,
        'human_readable': human_readable,
        'human_to_bytes': human_to_bytes,
        'zip': zip,
        'zip_longest': zip_longest,
    }
    return filters