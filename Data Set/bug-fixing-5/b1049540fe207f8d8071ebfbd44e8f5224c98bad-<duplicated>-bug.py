def duplicated(self, subset=None, keep='first'):
    "\n        Return boolean Series denoting duplicate rows, optionally only\n        considering certain columns.\n\n        Parameters\n        ----------\n        subset : column label or sequence of labels, optional\n            Only consider certain columns for identifying duplicates, by\n            default use all of the columns\n        keep : {'first', 'last', False}, default 'first'\n            Determines which duplicates (if any) to mark.\n\n            - ``first`` : Mark duplicates as ``True`` except for the first occurrence.\n            - ``last`` : Mark duplicates as ``True`` except for the last occurrence.\n            - False : Mark all duplicates as ``True``.\n\n        Returns\n        -------\n        Series\n        "
    from pandas.core.sorting import get_group_index
    from pandas._libs.hashtable import duplicated_int64, _SIZE_HINT_LIMIT
    if self.empty:
        return Series(dtype=bool)

    def f(vals):
        (labels, shape) = algorithms.factorize(vals, size_hint=min(len(self), _SIZE_HINT_LIMIT))
        return (labels.astype('i8', copy=False), len(shape))
    if (subset is None):
        subset = self.columns
    elif ((not np.iterable(subset)) or isinstance(subset, str) or (isinstance(subset, tuple) and (subset in self.columns))):
        subset = (subset,)
    diff = Index(subset).difference(self.columns)
    if (not diff.empty):
        raise KeyError(diff)
    vals = (col.values for (name, col) in self.items() if (name in subset))
    (labels, shape) = map(list, zip(*map(f, vals)))
    ids = get_group_index(labels, shape, sort=False, xnull=False)
    return Series(duplicated_int64(ids, keep), index=self.index)