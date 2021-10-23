def add(self, cell):
    'Append a cell into the stack.\n\n        Parameters\n        ----------\n        cell : rnn cell\n        '
    self._cells.append(cell)
    if self._override_cell_params:
        assert cell._own_params, 'Either specify params for SequentialRNNCell or child cells, not both.'
        cell.params._params.update(self.params._params)
    self.params._params.update(cell.params._params)