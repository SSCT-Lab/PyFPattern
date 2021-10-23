def fake_headers(self, num_docs, num_terms, num_nnz):
    'Write "fake" headers to file.\n\n        Parameters\n        ----------\n        num_docs : int\n            Number of documents in corpus\n        num_terms : int\n            Number of term in corpus\n        num_nnz : int\n            Number of non-zero elements in corpus\n\n        '
    stats = ('%i %i %i' % (num_docs, num_terms, num_nnz))
    if (len(stats) > 50):
        raise ValueError('Invalid stats: matrix too large!')
    self.fout.seek(len(MmWriter.HEADER_LINE))
    self.fout.write(utils.to_utf8(stats))