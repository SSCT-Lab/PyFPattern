

def value_counts(self, dropna=True):
    "\n        Returns a Series containing counts of each interval.\n\n        Parameters\n        ----------\n        dropna : bool, default True\n            Don't include counts of NaN.\n\n        Returns\n        -------\n        counts : Series\n\n        See Also\n        --------\n        Series.value_counts\n        "
    return value_counts(np.asarray(self), dropna=dropna)
