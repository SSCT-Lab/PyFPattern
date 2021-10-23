def process(path, fromfile, tofile, processor_function, hash_db, pxi_hashes):
    fullfrompath = os.path.join(path, fromfile)
    fulltopath = os.path.join(path, tofile)
    current_hash = get_hash(fullfrompath, fulltopath)
    if (current_hash == hash_db.get(normpath(fullfrompath), None)):
        file_changed = False
    else:
        file_changed = True
    pxi_changed = False
    pxi_dependencies = get_pxi_dependencies(fullfrompath)
    for pxi in pxi_dependencies:
        pxi_hash = get_hash(pxi, None)
        if (pxi_hash == hash_db.get(normpath(pxi), None)):
            continue
        else:
            pxi_hashes[normpath(pxi)] = pxi_hash
            pxi_changed = True
    if ((not file_changed) and (not pxi_changed)):
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