def load(self, fname):
    fname_dict = (fname + '.d')
    if (not (os.path.exists(fname) and os.path.exists(fname_dict))):
        raise IOError(("Can't find index files '%s' and '%s' - Unable to restore AnnoyIndexer state." % (fname, fname_dict)))
    else:
        with smart_open(fname_dict) as f:
            d = _pickle.loads(f.read())
        self.num_trees = d['num_trees']
        self.index = AnnoyIndex(d['f'])
        self.index.load(fname)
        self.labels = d['labels']