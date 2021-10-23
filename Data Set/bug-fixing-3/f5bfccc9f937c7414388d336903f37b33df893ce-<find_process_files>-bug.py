def find_process_files(root_dir):
    hash_db = load_hashes(HASH_FILE)
    for (cur_dir, dirs, files) in os.walk(root_dir):
        for filename in files:
            in_file = os.path.join(cur_dir, (filename + '.in'))
            if (filename.endswith('.pyx') and os.path.isfile(in_file)):
                continue
            for (fromext, function) in rules.items():
                if filename.endswith(fromext):
                    toext = '.c'
                    with open(os.path.join(cur_dir, filename), 'rb') as f:
                        data = f.read()
                        m = re.search(b'^\\s*#\\s*distutils:\\s*language\\s*=\\s*c\\+\\+\\s*$', data, (re.I | re.M))
                        if m:
                            toext = '.cxx'
                    fromfile = filename
                    tofile = (filename[:(- len(fromext))] + toext)
                    process(cur_dir, fromfile, tofile, function, hash_db)
                    save_hashes(hash_db, HASH_FILE)