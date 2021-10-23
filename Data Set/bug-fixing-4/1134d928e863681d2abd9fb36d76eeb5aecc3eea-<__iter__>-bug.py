def __iter__(self):
    'Return all outputs in a list'
    return (self[i] for i in self.list_outputs())