def construct_author2doc(doc2author):
    'Make a mapping from author IDs to document IDs.'
    authors_ids = set()
    for (d, a_doc_ids) in doc2author.items():
        for a in a_doc_ids:
            authors_ids.add(a)
    author2doc = {
        
    }
    for a in authors_ids:
        author2doc[a] = []
        for (d, a_ids) in doc2author.items():
            if (a in a_ids):
                author2doc[a].append(d)
    return author2doc