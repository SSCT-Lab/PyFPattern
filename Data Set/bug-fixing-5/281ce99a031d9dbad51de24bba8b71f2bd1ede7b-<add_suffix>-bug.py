def add_suffix(self, suffix):
    '\n        Concatenate suffix string with panel items names.\n\n        Parameters\n        ----------\n        suffix : string\n\n        Returns\n        -------\n        with_suffix : type of caller\n        '
    new_data = self._data.add_suffix(suffix)
    return self._constructor(new_data).__finalize__(self)