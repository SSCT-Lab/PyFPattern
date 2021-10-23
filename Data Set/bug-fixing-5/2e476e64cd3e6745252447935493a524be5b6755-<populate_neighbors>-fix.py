def populate_neighbors(self, data):
    if data.startswith('ERROR'):
        return dict()
    lines = data.split('\n')
    regex = re.compile('(\\S+)\\s+(\\S+)\\s+\\d+\\s+\\w+\\s+(\\S+)')
    objects = dict()
    for item in data.split('\n')[4:(- 1)]:
        match = regex.match(item)
        if match:
            nbor = {
                'host': match.group(1),
                'port': match.group(3),
            }
            if (match.group(2) not in objects):
                objects[match.group(2)] = []
            objects[match.group(2)].append(nbor)
    return objects