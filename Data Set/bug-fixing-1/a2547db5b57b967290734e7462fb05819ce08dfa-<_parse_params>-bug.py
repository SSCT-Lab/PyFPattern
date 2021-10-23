

def _parse_params(term):
    'Safely split parameter term to preserve spaces'
    keys = ['key', 'section', 'file', 're']
    params = {
        
    }
    for k in keys:
        params[k] = ''
    thiskey = 'key'
    for (idp, phrase) in enumerate(term.split()):
        for k in keys:
            if (('%s=' % k) in phrase):
                thiskey = k
        if ((idp == 0) or (not params[thiskey])):
            params[thiskey] = phrase
        else:
            params[thiskey] += (' ' + phrase)
    rparams = [params[x] for x in keys if params[x]]
    return rparams
