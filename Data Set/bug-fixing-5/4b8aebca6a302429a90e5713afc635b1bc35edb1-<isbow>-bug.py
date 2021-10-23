def isbow(vec):
    '\n    Checks if vector passed is in bag of words representation or not.\n    Vec is considered to be in bag of words format if it is 2-tuple format.\n    '
    if scipy.sparse.issparse(vec):
        vec = vec.todense().tolist()
    try:
        (id_, val_) = vec[0]
        (int(id_), float(val_))
    except IndexError:
        return True
    except (ValueError, TypeError):
        return False
    return True