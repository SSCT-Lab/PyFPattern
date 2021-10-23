def fake_headers(self, num_docs, num_terms, num_nnz):
    stats = ('%i %i %i' % (num_docs, num_terms, num_nnz))
    if (len(stats) > 50):
        raise ValueError('Invalid stats: matrix too large!')
    self.fout.seek(len(MmWriter.HEADER_LINE))
    self.fout.write(utils.to_utf8(stats))