def construct_doc2author(corpus, author2doc):
    'Make a mapping from document IDs to author IDs.'
    doc2author = {
        
    }
    for (d, _) in enumerate(corpus):
        author_ids = []
        for (a, a_doc_ids) in author2doc.items():
            if (d in a_doc_ids):
                author_ids.append(a)
        doc2author[d] = author_ids
    return doc2author