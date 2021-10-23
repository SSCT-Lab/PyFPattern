def process(path, fromfile, tofile, processor_function, hash_db):
    fullfrompath = os.path.join(path, fromfile)
    fulltopath = os.path.join(path, tofile)
    current_hash = get_hash(fullfrompath, fulltopath)
    if (current_hash == hash_db.get(normpath(fullfrompath), None)):
        print(('%s has not changed' % fullfrompath))
        return
    orig_cwd = os.getcwd()
    try:
        os.chdir(path)
        print(('Processing %s' % fullfrompath))
        processor_function(fromfile, tofile)
    finally:
        os.chdir(orig_cwd)
    current_hash = get_hash(fullfrompath, fulltopath)
    hash_db[normpath(fullfrompath)] = current_hash