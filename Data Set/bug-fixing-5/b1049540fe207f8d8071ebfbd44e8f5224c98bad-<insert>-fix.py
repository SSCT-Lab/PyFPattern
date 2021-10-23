def insert(self, loc, column, value, allow_duplicates=False):
    '\n        Insert column into DataFrame at specified location.\n\n        Raises a ValueError if `column` is already contained in the DataFrame,\n        unless `allow_duplicates` is set to True.\n\n        Parameters\n        ----------\n        loc : int\n            Insertion index. Must verify 0 <= loc <= len(columns).\n        column : str, number, or hashable object\n            Label of the inserted column.\n        value : int, Series, or array-like\n        allow_duplicates : bool, optional\n        '
    self._ensure_valid_index(value)
    value = self._sanitize_column(column, value, broadcast=False)
    self._data.insert(loc, column, value, allow_duplicates=allow_duplicates)