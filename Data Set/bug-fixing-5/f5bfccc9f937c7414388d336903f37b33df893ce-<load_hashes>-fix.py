def load_hashes(filename):
    if os.path.isfile(filename):
        hashes = {
            
        }
        with open(filename, 'r') as f:
            for line in f:
                (filename, inhash, outhash) = line.split()
                if (outhash == 'None'):
                    outhash = None
                hashes[filename] = (inhash, outhash)
    else:
        hashes = {
            
        }
    return hashes