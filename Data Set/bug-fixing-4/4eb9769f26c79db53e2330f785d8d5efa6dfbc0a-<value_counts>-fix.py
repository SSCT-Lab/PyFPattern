def value_counts(self, dropna=True):
    "\n        Returns a Series containing counts of each category.\n\n        Every category will have an entry, even those with a count of 0.\n\n        Parameters\n        ----------\n        dropna : boolean, default True\n            Don't include counts of NaN.\n\n        Returns\n        -------\n        counts : Series\n\n        See Also\n        --------\n        Series.value_counts\n\n        "
    from numpy import bincount
    from pandas import Series, CategoricalIndex
    (code, cat) = (self._codes, self.categories)
    (ncat, mask) = (len(cat), (0 <= code))
    (ix, clean) = (np.arange(ncat), mask.all())
    if (dropna or clean):
        obs = (code if clean else code[mask])
        count = bincount(obs, minlength=(ncat or None))
    else:
        count = bincount(np.where(mask, code, ncat))
        ix = np.append(ix, (- 1))
    ix = self._constructor(ix, dtype=self.dtype, fastpath=True)
    return Series(count, index=CategoricalIndex(ix), dtype='int64')