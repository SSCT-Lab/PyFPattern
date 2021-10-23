def write_conllu(docs, file_):
    if (not Token.has_extension('get_conllu_lines')):
        Token.set_extension('get_conllu_lines', method=get_token_conllu)
    if (not Token.has_extension('begins_fused')):
        Token.set_extension('begins_fused', default=False)
    if (not Token.has_extension('inside_fused')):
        Token.set_extension('inside_fused', default=False)
    merger = Matcher(docs[0].vocab)
    merger.add('SUBTOK', None, [{
        'DEP': 'subtok',
        'op': '+',
    }])
    for (i, doc) in enumerate(docs):
        matches = []
        if doc.is_parsed:
            matches = merger(doc)
        spans = [doc[start:(end + 1)] for (_, start, end) in matches]
        seen_tokens = set()
        with doc.retokenize() as retokenizer:
            for span in spans:
                span_tokens = set(range(span.start, span.end))
                if (not span_tokens.intersection(seen_tokens)):
                    retokenizer.merge(span)
                    seen_tokens.update(span_tokens)
        file_.write('# newdoc id = {i}\n'.format(i=i))
        for (j, sent) in enumerate(doc.sents):
            file_.write('# sent_id = {i}.{j}\n'.format(i=i, j=j))
            file_.write('# text = {text}\n'.format(text=sent.text))
            for (k, token) in enumerate(sent):
                if ((token.head.i > sent[(- 1)].i) or (token.head.i < sent[0].i)):
                    for word in doc[(sent[0].i - 10):sent[0].i]:
                        print(word.i, word.head.i, word.text, word.dep_)
                    for word in sent:
                        print(word.i, word.head.i, word.text, word.dep_)
                    for word in doc[sent[(- 1)].i:(sent[(- 1)].i + 10)]:
                        print(word.i, word.head.i, word.text, word.dep_)
                    raise ValueError(('Invalid parse: head outside sentence (%s)' % token.text))
                file_.write((token._.get_conllu_lines(k) + '\n'))
            file_.write('\n')