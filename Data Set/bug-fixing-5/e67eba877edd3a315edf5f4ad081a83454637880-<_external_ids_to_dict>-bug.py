def _external_ids_to_dict(text):
    d = {
        
    }
    for l in text.splitlines():
        if l:
            (k, v) = l.split('=')
            d[k] = v
    return d