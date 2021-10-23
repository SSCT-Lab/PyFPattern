def do_estep(self, chunk, author2doc, doc2author, rhot, state=None, chunk_doc_idx=None):
    'Performs inference (E-step) on a chunk of documents, and accumulate the collected sufficient statistics.\n\n        Parameters\n        ----------\n        chunk : iterable of list of (int, float)\n            Corpus in BoW format.\n        author2doc : dict of (str, list of int), optional\n            A dictionary where keys are the names of authors and values are lists of document IDs that the author\n            contributes to.\n        doc2author : dict of (int, list of str), optional\n            A dictionary where the keys are document IDs and the values are lists of author names.\n        rhot : float\n            Value of rho for conducting inference on documents.\n        state : int, optional\n            Initializes the state for a new E iteration.\n        chunk_doc_idx : numpy.ndarray, optional\n            Assigns the value for document index.\n\n        Returns\n        -------\n        float\n            Value of gamma for training of model.\n\n        '
    if (state is None):
        state = self.state
    (gamma, sstats) = self.inference(chunk, author2doc, doc2author, rhot, collect_sstats=True, chunk_doc_idx=chunk_doc_idx)
    state.sstats += sstats
    state.numdocs += len(chunk)
    return gamma