def idxmin(self, axis=0, skipna=True):
    "\n        Return index of first occurrence of minimum over requested axis.\n        NA/null values are excluded.\n\n        Parameters\n        ----------\n        axis : {0 or 'index', 1 or 'columns'}, default 0\n            The axis to use. 0 or 'index' for row-wise, 1 or 'columns' for column-wise\n        skipna : boolean, default True\n            Exclude NA/null values. If an entire row/column is NA, the result\n            will be NA.\n\n        Returns\n        -------\n        Series\n            Indexes of minima along the specified axis.\n\n        Raises\n        ------\n        ValueError\n            * If the row/column is empty\n\n        See Also\n        --------\n        Series.idxmin\n\n        Notes\n        -----\n        This method is the DataFrame version of ``ndarray.argmin``.\n        "
    axis = self._get_axis_number(axis)
    indices = nanops.nanargmin(self.values, axis=axis, skipna=skipna)
    index = self._get_axis(axis)
    result = [(index[i] if (i >= 0) else np.nan) for i in indices]
    return Series(result, index=self._get_agg_axis(axis))