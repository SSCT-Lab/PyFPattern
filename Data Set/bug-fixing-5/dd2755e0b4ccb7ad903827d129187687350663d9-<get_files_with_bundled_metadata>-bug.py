def get_files_with_bundled_metadata(paths):
    with_metadata = set()
    for path in paths:
        if (path == 'test/sanity/code-smell/update-bundled.py'):
            continue
        with open(path, 'rb') as f:
            body = f.read()
        if BUNDLED_RE.search(body):
            with_metadata.add(path)
    return with_metadata