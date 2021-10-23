def _update_count(self, index):
    'Update num_update\n\n        Parameters:\n        index : int\n            The index to be updated.\n        '
    if (index not in self._index_update_count):
        self._index_update_count[index] = self.begin_num_update
    self._index_update_count[index] += 1
    self.num_update = max(self._index_update_count[index], self.num_update)