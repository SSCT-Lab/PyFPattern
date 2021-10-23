

def read_iob(raw_sents):
    sentences = []
    for line in raw_sents:
        if (not line.strip()):
            continue
        tokens = [re.split('[^\\w\\-]', line.strip())]
        if (len(tokens[0]) == 3):
            (words, pos, iob) = zip(*tokens)
        elif (len(tokens[0]) == 2):
            (words, iob) = zip(*tokens)
            pos = (['-'] * len(words))
        else:
            raise ValueError('The iob/iob2 file is not formatted correctly. Try checking whitespace and delimiters.')
        biluo = iob_to_biluo(iob)
        sentences.append([{
            'orth': w,
            'tag': p,
            'ner': ent,
        } for (w, p, ent) in zip(words, pos, biluo)])
    sentences = [{
        'tokens': sent,
    } for sent in sentences]
    paragraphs = [{
        'sentences': [sent],
    } for sent in sentences]
    docs = [{
        'id': 0,
        'paragraphs': [para],
    } for para in paragraphs]
    return docs
