def log_perplexity(self, chunk, chunk_doc_idx=None, total_docs=None):
    '\n        Calculate and return per-word likelihood bound, using the `chunk` of\n        documents as evaluation corpus. Also output the calculated statistics. incl.\n        perplexity=2^(-bound), to log at INFO level.\n\n        '
    if (total_docs is None):
        total_docs = len(chunk)
    corpus_words = sum((cnt for document in chunk for (_, cnt) in document))
    subsample_ratio = ((1.0 * total_docs) / len(chunk))
    perwordbound = (self.bound(chunk, chunk_doc_idx, subsample_ratio=subsample_ratio) / (subsample_ratio * corpus_words))
    logger.info('%.3f per-word bound, %.1f perplexity estimate based on a corpus of %i documents with %i words', perwordbound, np.exp2((- perwordbound)), len(chunk), corpus_words)
    return perwordbound