def get_bundled_metadata(filename):
    "\n    Retrieve the metadata about a bundled library from a python file\n\n    :arg filename: The filename to look inside for the metadata\n    :raises ValueError: If we're unable to extract metadata from the file\n    :returns: The metadata from the python file\n    "
    with open(filename, 'r') as module:
        for line in module:
            if line.strip().startswith('_BUNDLED_METADATA'):
                data = line[line.index('{'):].strip()
                break
        else:
            raise ValueError('Unable to check bundled library for update.  Please add _BUNDLED_METADATA dictionary to the library file with information on pypi name and bundled version.')
        metadata = json.loads(data)
    return metadata