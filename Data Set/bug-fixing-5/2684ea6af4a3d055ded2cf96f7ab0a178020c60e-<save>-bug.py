def save(self, fname, protocol=2):
    fname_dict = (fname + '.d')
    self.index.save(fname)
    d = {
        'f': self.model.vector_size,
        'num_trees': self.num_trees,
        'labels': self.labels,
    }
    with smart_open(fname_dict, 'wb') as fout:
        _pickle.dump(d, fout, protocol=protocol)