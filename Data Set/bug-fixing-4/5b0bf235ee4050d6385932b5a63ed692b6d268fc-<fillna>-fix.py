def fillna(self, value=None, method=None, limit=None):
    "\n        Fill NA/NaN values using the specified method.\n\n        Parameters\n        ----------\n        value : scalar, array-like\n            If a scalar value is passed it is used to fill all missing values.\n            Alternatively, an array-like 'value' can be given. It's expected\n            that the array-like have the same length as 'self'.\n        method : {'backfill', 'bfill', 'pad', 'ffill', None}, default None\n            Method to use for filling holes in reindexed Series\n            pad / ffill: propagate last valid observation forward to next valid\n            backfill / bfill: use NEXT valid observation to fill gap.\n        limit : int, default None\n            If method is specified, this is the maximum number of consecutive\n            NaN values to forward/backward fill. In other words, if there is\n            a gap with more than this number of consecutive NaNs, it will only\n            be partially filled. If method is not specified, this is the\n            maximum number of entries along the entire axis where NaNs will be\n            filled.\n\n        Returns\n        -------\n        ExtensionArray\n            With NA/NaN filled.\n        "
    (value, method) = validate_fillna_kwargs(value, method)
    mask = self.isna()
    if is_array_like(value):
        if (len(value) != len(self)):
            raise ValueError("Length of 'value' does not match. Got ({})  expected {}".format(len(value), len(self)))
        value = value[mask]
    if mask.any():
        if (method is not None):
            func = (pad_1d if (method == 'pad') else backfill_1d)
            new_values = func(self.astype(object), limit=limit, mask=mask)
            new_values = self._from_sequence(new_values, dtype=self.dtype)
        else:
            new_values = self.copy()
            new_values[mask] = value
    else:
        new_values = self.copy()
    return new_values