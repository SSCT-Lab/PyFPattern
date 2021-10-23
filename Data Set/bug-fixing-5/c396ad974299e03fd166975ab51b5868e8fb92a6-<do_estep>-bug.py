def do_estep(self, chunk, author2doc, doc2author, rhot, state=None, chunk_doc_idx=None):
    '\n        Perform inference on a chunk of documents, and accumulate the collected\n        sufficient statistics in `state` (or `self.state` if None).\n\n        '
    if (state is None):
        state = self.state
    (gamma, sstats) = self.inference(chunk, author2doc, doc2author, rhot, collect_sstats=True, chunk_doc_idx=chunk_doc_idx)
    state.sstats += sstats
    state.numdocs += len(chunk)
    return gamma