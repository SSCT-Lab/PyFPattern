def docbyoffset(self, offset):
    'Return document at file offset `offset` (in bytes)'
    if (offset == (- 1)):
        return []
    if isinstance(self.input, string_types):
        (fin, close_fin) = (utils.smart_open(self.input), True)
    else:
        (fin, close_fin) = (self.input, False)
    fin.seek(offset)
    (previd, document) = ((- 1), [])
    for line in fin:
        (docid, termid, val) = line.split()
        if (not self.transposed):
            (termid, docid) = (docid, termid)
        (docid, termid, val) = ((int(docid) - 1), (int(termid) - 1), float(val))
        assert (previd <= docid), 'matrix columns must come in ascending order'
        if (docid != previd):
            if (previd >= 0):
                break
            previd = docid
        document.append((termid, val))
    if close_fin:
        fin.close()
    return document