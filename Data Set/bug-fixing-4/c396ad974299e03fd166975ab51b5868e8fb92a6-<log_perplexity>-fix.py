def log_perplexity(self, chunk, chunk_doc_idx=None, total_docs=None):
    'Calculate per-word likelihood bound, using the `chunk` of documents as evaluation corpus.\n\n        Parameters\n        ----------\n        chunk : iterable of list of (int, float)\n            Corpus in BoW format.\n        chunk_doc_idx : numpy.ndarray, optional\n            Assigns the value for document index.\n        total_docs : int, optional\n            Initializes the value for total number of documents.\n\n        Returns\n        -------\n        float\n            Value of per-word likelihood bound.\n\n        '
    if (total_docs is None):
        total_docs = len(chunk)
    corpus_words = sum((cnt for document in chunk for (_, cnt) in document))
    subsample_ratio = ((1.0 * total_docs) / len(chunk))
    perwordbound = (self.bound(chunk, chunk_doc_idx, subsample_ratio=subsample_ratio) / (subsample_ratio * corpus_words))
    logger.info('%.3f per-word bound, %.1f perplexity estimate based on a corpus of %i documents with %i words', perwordbound, np.exp2((- perwordbound)), len(chunk), corpus_words)
    return perwordbound