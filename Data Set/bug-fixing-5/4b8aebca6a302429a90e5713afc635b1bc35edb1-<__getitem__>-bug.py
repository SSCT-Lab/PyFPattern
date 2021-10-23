def __getitem__(self, document_index):
    '\n        Return a single document in the corpus by its index (between 0 and `len(self)-1`).\n        '
    indprev = self.sparse.indptr[document_index]
    indnow = self.sparse.indptr[(document_index + 1)]
    return list(zip(self.sparse.indices[indprev:indnow], self.sparse.data[indprev:indnow]))