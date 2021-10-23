@classmethod
def from_tuples(cls, data, closed='right', name=None, copy=False, dtype=None):
    "\n        Construct an IntervalIndex from a list/array of tuples\n\n        Parameters\n        ----------\n        data : array-like (1-dimensional)\n            Array of tuples\n        closed : {'left', 'right', 'both', 'neither'}, default 'right'\n            Whether the intervals are closed on the left-side, right-side, both\n            or neither.\n        name : object, optional\n            Name to be stored in the index.\n        copy : boolean, default False\n            by-default copy the data, this is compat only and ignored\n        dtype : dtype or None, default None\n            If None, dtype will be inferred\n\n            .. versionadded:: 0.23.0\n\n        Examples\n        --------\n        >>>  pd.IntervalIndex.from_tuples([(0, 1), (1, 2)])\n        IntervalIndex([(0, 1], (1, 2]],\n                      closed='right', dtype='interval[int64]')\n\n        See Also\n        --------\n        interval_range : Function to create a fixed frequency IntervalIndex\n        IntervalIndex.from_arrays : Construct an IntervalIndex from a left and\n                                    right array\n        IntervalIndex.from_breaks : Construct an IntervalIndex from an array of\n                                    splits\n        "
    if len(data):
        (left, right) = ([], [])
    else:
        left = right = data
    for d in data:
        if isna(d):
            lhs = rhs = np.nan
        else:
            try:
                (lhs, rhs) = d
            except ValueError:
                msg = 'IntervalIndex.from_tuples requires tuples of length 2, got {tpl}'.format(tpl=d)
                raise ValueError(msg)
            except TypeError:
                msg = 'IntervalIndex.from_tuples received an invalid item, {tpl}'.format(tpl=d)
                raise TypeError(msg)
        left.append(lhs)
        right.append(rhs)
    return cls.from_arrays(left, right, closed, name=name, copy=False, dtype=dtype)