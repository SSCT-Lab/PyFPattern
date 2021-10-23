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
        data = to_text(b_data, errors='surrogate_or_strict').splitlines()
    except UnicodeError:
        data = []
        for line in b_data.splitlines():
            if (line and (line[0] in self.b_COMMENT_MARKERS)):
                data.append('')
            else:
                data.append(to_text(line, errors='surrogate_or_strict'))
    self._parse(data)