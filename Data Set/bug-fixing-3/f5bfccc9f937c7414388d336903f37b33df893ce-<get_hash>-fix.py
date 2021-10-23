def get_hash(frompath, topath):
    from_hash = sha1_of_file(frompath)
    if topath:
        to_hash = (sha1_of_file(topath) if os.path.exists(topath) else None)
    else:
        to_hash = None
    return (from_hash, to_hash)