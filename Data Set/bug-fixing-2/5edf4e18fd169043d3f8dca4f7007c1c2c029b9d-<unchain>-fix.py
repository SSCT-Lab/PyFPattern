

def unchain(self):
    'Purges in/out nodes and this function node itself from the graph.'
    if self._is_chainerx_fallback_mode:
        raise NotImplementedError('Unchaining is not yet supported in ChainerX fallback mode.')
    for y in self.outputs:
        y_ref = y()
        if (y_ref is not None):
            y_ref.unchain()
    self.inputs = None
    self.outputs = None
