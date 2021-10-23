def to_tuples(self, na_tuple=True):
    "\n        Return an Index of tuples of the form (left, right)\n\n        Parameters\n        ----------\n        na_tuple : boolean, default True\n            Returns NA as a tuple if True, ``(nan, nan)``, or just as the NA\n            value itself if False, ``nan``.\n\n            ..versionadded:: 0.23.0\n\n        Examples\n        --------\n        >>>  idx = pd.IntervalIndex.from_arrays([0, np.nan, 2], [1, np.nan, 3])\n        >>>  idx.to_tuples()\n        Index([(0.0, 1.0), (nan, nan), (2.0, 3.0)], dtype='object')\n        >>>  idx.to_tuples(na_tuple=False)\n        Index([(0.0, 1.0), nan, (2.0, 3.0)], dtype='object')\n        "
    tuples = com._asarray_tuplesafe(zip(self.left, self.right))
    if (not na_tuple):
        tuples = np.where((~ self._isnan), tuples, np.nan)
    return Index(tuples)