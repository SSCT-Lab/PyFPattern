def get_bundled_metadata(filename):
    with open(filename, 'r') as module:
        for line in module:
            if line.strip().startswith('_BUNDLED_METADATA'):
                data = line[line.index('{'):].strip()
                break
        else:
            raise ValueError('Unable to check bundled library for update.  Please add _BUNDLED_METADATA dictionary to the library file with information on pypi name and bundled version.')
        metadata = json.loads(data)
    return metadata