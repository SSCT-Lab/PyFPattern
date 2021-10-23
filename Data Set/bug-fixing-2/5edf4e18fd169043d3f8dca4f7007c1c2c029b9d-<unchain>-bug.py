

def unchain(self):
    'Purges in/out nodes and this function node itself from the graph.'
    for y in self.outputs:
        y_ref = y()
        if (y_ref is not None):
            y_ref.unchain()
    self.inputs = None
