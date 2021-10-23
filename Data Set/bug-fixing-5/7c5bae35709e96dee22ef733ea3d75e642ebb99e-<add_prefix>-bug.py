def add_prefix(self, prefix):
    '\n        Concatenate prefix string with panel items names.\n\n        Parameters\n        ----------\n        prefix : string\n\n        Returns\n        -------\n        with_prefix : type of caller\n        '
    new_data = self._data.add_prefix(prefix)
    return self._constructor(new_data).__finalize__(self)