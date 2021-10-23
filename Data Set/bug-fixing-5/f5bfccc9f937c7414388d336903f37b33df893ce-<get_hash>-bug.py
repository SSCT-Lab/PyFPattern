def get_hash(frompath, topath):
    from_hash = sha1_of_file(frompath)
    to_hash = (sha1_of_file(topath) if os.path.exists(topath) else None)
    return (from_hash, to_hash)