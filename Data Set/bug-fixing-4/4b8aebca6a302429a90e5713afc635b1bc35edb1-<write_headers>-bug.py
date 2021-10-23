def write_headers(self, num_docs, num_terms, num_nnz):
    self.fout.write(MmWriter.HEADER_LINE)
    if (num_nnz < 0):
        logger.info('saving sparse matrix to %s', self.fname)
        self.fout.write(utils.to_utf8(((' ' * 50) + '\n')))
    else:
        logger.info('saving sparse %sx%s matrix with %i non-zero entries to %s', num_docs, num_terms, num_nnz, self.fname)
        self.fout.write(utils.to_utf8(('%s %s %s\n' % (num_docs, num_terms, num_nnz))))
    self.last_docno = (- 1)
    self.headers_written = True