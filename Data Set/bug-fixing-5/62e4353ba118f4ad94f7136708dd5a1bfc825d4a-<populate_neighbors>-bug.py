def populate_neighbors(self, data):
    objects = dict()
    if isinstance(data, str):
        if data.startswith('ERROR'):
            return dict()
        lines = data.split('\n')
        regex = re.compile('(\\S+)\\s+(\\S+)\\s+\\d+\\s+\\w+\\s+(\\S+)')
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
    elif isinstance(data, dict):
        data = data['TABLE_nbor']['ROW_nbor']
        if isinstance(data, dict):
            data = [data]
        for item in data:
            local_intf = item['l_port_id']
            if (local_intf not in objects):
                objects[local_intf] = list()
            nbor = dict()
            nbor['port'] = item['port_id']
            nbor['host'] = item['chassis_id']
            objects[local_intf].append(nbor)
    return objects