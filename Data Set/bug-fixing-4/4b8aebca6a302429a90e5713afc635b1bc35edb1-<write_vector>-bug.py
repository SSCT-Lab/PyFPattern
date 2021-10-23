def write_vector(self, docno, vector):
    '\n        Write a single sparse vector to the file.\n\n        Sparse vector is any iterable yielding (field id, field value) pairs.\n        '
    assert self.headers_written, 'must write Matrix Market file headers before writing data!'
    assert (self.last_docno < docno), ('documents %i and %i not in sequential order!' % (self.last_docno, docno))
    vector = sorted(((i, w) for (i, w) in vector if (abs(w) > 1e-12)))
    for (termid, weight) in vector:
        self.fout.write(utils.to_utf8(('%i %i %s\n' % ((docno + 1), (termid + 1), weight))))
    self.last_docno = docno
    return ((vector[(- 1)][0], len(vector)) if vector else ((- 1), 0))