def sparse2full(doc, length):
    '\n    Convert a document in sparse document format (=sequence of 2-tuples) into a dense\n    np array (of size `length`).\n\n    This is the mirror function to `full2sparse`.\n\n    '
    result = np.zeros(length, dtype=np.float32)
    doc = ((int(id_), float(val_)) for (id_, val_) in doc)
    doc = dict(doc)
    result[list(doc)] = list(itervalues(doc))
    return result