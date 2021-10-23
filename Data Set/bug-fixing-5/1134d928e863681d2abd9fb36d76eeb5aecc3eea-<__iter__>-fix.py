def __iter__(self):
    'Returns all outputs in a list'
    return (self[i] for i in self.list_outputs())