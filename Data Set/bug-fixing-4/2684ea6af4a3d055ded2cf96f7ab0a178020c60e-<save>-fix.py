def save(self, fname, protocol=2):
    "Save AnnoyIndexer instance.\n\n        Parameters\n        ----------\n        fname : str\n            Path to output file, will produce 2 files: `fname` - parameters and `fname`.d - :class:`~annoy.AnnoyIndex`.\n        protocol : int, optional\n            Protocol for pickle.\n\n        Notes\n        -----\n        This method save **only** index (**model isn't preserved**).\n\n        "
    fname_dict = (fname + '.d')
    self.index.save(fname)
    d = {
        'f': self.model.vector_size,
        'num_trees': self.num_trees,
        'labels': self.labels,
    }
    with smart_open(fname_dict, 'wb') as fout:
        _pickle.dump(d, fout, protocol=protocol)