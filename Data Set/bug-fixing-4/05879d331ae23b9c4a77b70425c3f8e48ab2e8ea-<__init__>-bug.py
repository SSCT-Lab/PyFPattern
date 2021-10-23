def __init__(self, loader, groups, filename=C.DEFAULT_HOST_LIST):
    self.filename = filename
    self.hosts = {
        
    }
    self.patterns = {
        
    }
    self.groups = groups
    if loader:
        (b_data, private) = loader._get_file_contents(filename)
    else:
        with open(filename, 'rb') as fh:
            b_data = fh.read()
    try:
        data = to_text(b_data, errors='surrogate_or_strict')
        data = [line for line in data.splitlines() if (not (line.startswith(';') or line.startswith('#')))]
    except UnicodeError:
        data = [to_text(line, errors='surrogate_or_strict') for line in b_data.splitlines() if (not (line.startswith(b';') or line.startswith(b'#')))]
    self._parse(data)