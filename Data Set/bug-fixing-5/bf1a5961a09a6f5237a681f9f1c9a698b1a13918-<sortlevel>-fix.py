def sortlevel(self, level=0, ascending=True, sort_remaining=True):
    '\n        Sort MultiIndex at the requested level. The result will respect the\n        original ordering of the associated factor at that level.\n\n        Parameters\n        ----------\n        level : list-like, int or str, default 0\n            If a string is given, must be a name of the level\n            If list-like must be names or ints of levels.\n        ascending : boolean, default True\n            False to sort in descending order\n            Can also be a list to specify a directed ordering\n        sort_remaining : sort by the remaining levels after level.\n\n        Returns\n        -------\n        sorted_index : pd.MultiIndex\n            Resulting index\n        indexer : np.ndarray\n            Indices of output values in original index\n\n        '
    from pandas.core.groupby import _indexer_from_factorized
    if isinstance(level, (compat.string_types, int)):
        level = [level]
    level = [self._get_level_number(lev) for lev in level]
    sortorder = None
    if isinstance(ascending, list):
        if (not (len(level) == len(ascending))):
            raise ValueError('level must have same length as ascending')
        from pandas.core.groupby import _lexsort_indexer
        indexer = _lexsort_indexer(self.labels, orders=ascending)
    else:
        labels = list(self.labels)
        shape = list(self.levshape)
        primary = tuple((labels.pop((lev - i)) for (i, lev) in enumerate(level)))
        primshp = tuple((shape.pop((lev - i)) for (i, lev) in enumerate(level)))
        if sort_remaining:
            primary += (primary + tuple(labels))
            primshp += (primshp + tuple(shape))
        else:
            sortorder = level[0]
        indexer = _indexer_from_factorized(primary, primshp, compress=False)
        if (not ascending):
            indexer = indexer[::(- 1)]
    indexer = _ensure_platform_int(indexer)
    new_labels = [lab.take(indexer) for lab in self.labels]
    new_index = MultiIndex(labels=new_labels, levels=self.levels, names=self.names, sortorder=sortorder, verify_integrity=False)
    return (new_index, indexer)