def shift(self, periods: int=1, fill_value: object=None) -> ABCExtensionArray:
    '\n        Shift values by desired number.\n\n        Newly introduced missing values are filled with\n        ``self.dtype.na_value``.\n\n        .. versionadded:: 0.24.0\n\n        Parameters\n        ----------\n        periods : int, default 1\n            The number of periods to shift. Negative values are allowed\n            for shifting backwards.\n\n        fill_value : object, optional\n            The scalar value to use for newly introduced missing values.\n            The default is ``self.dtype.na_value``\n\n            .. versionadded:: 0.24.0\n\n        Returns\n        -------\n        shifted : ExtensionArray\n\n        Notes\n        -----\n        If ``self`` is empty or ``periods`` is 0, a copy of ``self`` is\n        returned.\n\n        If ``periods > len(self)``, then an array of size\n        len(self) is returned, with all values filled with\n        ``self.dtype.na_value``.\n        '
    if ((not len(self)) or (periods == 0)):
        return self.copy()
    if isna(fill_value):
        fill_value = self.dtype.na_value
    empty = self._from_sequence(([fill_value] * min(abs(periods), len(self))), dtype=self.dtype)
    if (periods > 0):
        a = empty
        b = self[:(- periods)]
    else:
        a = self[abs(periods):]
        b = empty
    return self._concat_same_type([a, b])