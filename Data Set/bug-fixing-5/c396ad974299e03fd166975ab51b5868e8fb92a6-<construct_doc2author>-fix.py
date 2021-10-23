def construct_doc2author(corpus, author2doc):
    'Create a mapping from document IDs to author IDs.\n\n    Parameters\n    ----------\n    corpus: iterable of list of (int, float)\n        Corpus in BoW format.\n    author2doc: dict of (str, list of int)\n        Mapping of authors to documents.\n\n    Returns\n    -------\n    dict of (int, list of str)\n        Document to Author mapping.\n\n    '
    doc2author = {
        
    }
    for (d, _) in enumerate(corpus):
        author_ids = []
        for (a, a_doc_ids) in author2doc.items():
            if (d in a_doc_ids):
                author_ids.append(a)
        doc2author[d] = author_ids
    return doc2author