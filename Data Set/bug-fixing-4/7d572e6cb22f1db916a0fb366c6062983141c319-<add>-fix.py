def add(self, cell):
    "Append a cell into the stack.\n\n        Parameters\n        ----------\n        cell : BaseRNNCell\n            The cell to be appended. During unroll, previous cell's output (or raw inputs if\n            no previous cell) is used as the input to this cell.\n        "
    self._cells.append(cell)
    if self._override_cell_params:
        assert cell._own_params, 'Either specify params for SequentialRNNCell or child cells, not both.'
        cell.params._params.update(self.params._params)
    self.params._params.update(cell.params._params)