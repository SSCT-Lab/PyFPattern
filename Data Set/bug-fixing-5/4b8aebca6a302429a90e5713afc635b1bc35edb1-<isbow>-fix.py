def isbow(vec):
    'Checks if vector passed is in BoW format.\n\n    Parameters\n    ----------\n    vec : object\n        Input vector in any format\n\n    Returns\n    -------\n    bool\n        True if vector in BoW format, False otherwise.\n\n    '
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