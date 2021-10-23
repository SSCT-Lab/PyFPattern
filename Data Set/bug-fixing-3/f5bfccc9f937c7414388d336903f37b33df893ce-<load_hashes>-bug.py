def load_hashes(filename):
    if os.path.isfile(filename):
        hashes = {
            
        }
        with open(filename, 'r') as f:
            for line in f:
                (filename, inhash, outhash) = line.split()
                hashes[filename] = (inhash, outhash)
    else:
        hashes = {
            
        }
    return hashes