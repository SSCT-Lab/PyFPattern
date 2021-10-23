def generate_sentence(sent):
    (id_, word, tag, head, dep, _) = sent
    sentence = {
        
    }
    tokens = []
    for (i, id) in enumerate(id_):
        token = {
            
        }
        token['orth'] = word[id]
        token['tag'] = tag[id]
        token['head'] = (head[id] - i)
        token['dep'] = dep[id]
        tokens.append(token)
    sentence['tokens'] = tokens
    return sentence