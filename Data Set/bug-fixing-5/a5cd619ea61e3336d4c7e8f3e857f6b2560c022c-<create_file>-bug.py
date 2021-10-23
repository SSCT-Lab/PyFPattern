def create_file(path, content):
    with open(path, 'wb') as f:
        f.write(content)
    return path