def generate_sentence(sent):
    (id_, word, tag, head, dep, _) = sent
    sentence = {
        
    }
    tokens = []
    for (i, id) in enumerate(id_):
        token = {
            
        }
        token['orth'] = word[i]
        token['tag'] = tag[i]
        token['head'] = (head[i] - id)
        token['dep'] = dep[i]
        tokens.append(token)
    sentence['tokens'] = tokens
    return sentence