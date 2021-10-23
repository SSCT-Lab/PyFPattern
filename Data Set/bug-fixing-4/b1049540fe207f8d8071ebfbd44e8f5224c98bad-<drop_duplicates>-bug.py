def drop_duplicates(self, subset=None, keep='first', inplace=False):
    "\n        Return DataFrame with duplicate rows removed, optionally only\n        considering certain columns. Indexes, including time indexes\n        are ignored.\n\n        Parameters\n        ----------\n        subset : column label or sequence of labels, optional\n            Only consider certain columns for identifying duplicates, by\n            default use all of the columns\n        keep : {'first', 'last', False}, default 'first'\n            Determines which duplicates (if any) to keep.\n            - ``first`` : Drop duplicates except for the first occurrence.\n            - ``last`` : Drop duplicates except for the last occurrence.\n            - False : Drop all duplicates.\n        inplace : bool, default False\n            Whether to drop duplicates in place or to return a copy\n\n        Returns\n        -------\n        DataFrame\n        "
    if self.empty:
        return self.copy()
    inplace = validate_bool_kwarg(inplace, 'inplace')
    duplicated = self.duplicated(subset, keep=keep)
    if inplace:
        (inds,) = (- duplicated)._ndarray_values.nonzero()
        new_data = self._data.take(inds)
        self._update_inplace(new_data)
    else:
        return self[(- duplicated)]