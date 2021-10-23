def __getitem__(self, document_index):
    'Get a single document in the corpus by its index.\n\n        Parameters\n        ----------\n        document_index : int\n            Index of document\n\n        Returns\n        -------\n        list of (int, number)\n            Document in BoW format.\n\n        '
    indprev = self.sparse.indptr[document_index]
    indnow = self.sparse.indptr[(document_index + 1)]
    return list(zip(self.sparse.indices[indprev:indnow], self.sparse.data[indprev:indnow]))