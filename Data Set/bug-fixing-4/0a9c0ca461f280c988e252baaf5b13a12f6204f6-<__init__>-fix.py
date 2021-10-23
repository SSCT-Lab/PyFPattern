def __init__(self, layers=[], name=None):
    self.layers = []
    self.model = None
    self.inputs = []
    self.outputs = []
    self._trainable = True
    self.inbound_nodes = []
    self.outbound_nodes = []
    self.built = False
    self._flattened_layers = None
    if (not name):
        prefix = 'sequential_'
        name = (prefix + str(K.get_uid(prefix)))
    self.name = name
    for layer in layers:
        self.add(layer)