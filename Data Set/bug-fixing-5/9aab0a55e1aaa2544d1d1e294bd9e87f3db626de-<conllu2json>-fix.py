def conllu2json(input_data, n_sents=10, use_morphology=False, lang=None, **_):
    '\n    Convert conllu files into JSON format for use with train cli.\n    use_morphology parameter enables appending morphology to tags, which is\n    useful for languages such as Spanish, where UD tags are not so rich.\n\n    Extract NER tags if available and convert them so that they follow\n    BILUO and the Wikipedia scheme\n    '
    docs = []
    sentences = []
    conll_data = read_conllx(input_data, use_morphology=use_morphology)
    checked_for_ner = False
    has_ner_tags = False
    for (i, example) in enumerate(conll_data):
        if (not checked_for_ner):
            has_ner_tags = is_ner(example.token_annotation.entities[0])
            checked_for_ner = True
        sentences.append(generate_sentence(example.token_annotation, has_ner_tags))
        if ((len(sentences) % n_sents) == 0):
            doc = create_doc(sentences, i)
            docs.append(doc)
            sentences = []
    if sentences:
        doc = create_doc(sentences, i)
        docs.append(doc)
    return docs