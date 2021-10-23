

def _external_ids_to_dict(text):
    if (not text):
        return None
    else:
        d = {
            
        }
        for l in text.splitlines():
            if l:
                (k, v) = l.split('=')
                d[k] = v
        return d
