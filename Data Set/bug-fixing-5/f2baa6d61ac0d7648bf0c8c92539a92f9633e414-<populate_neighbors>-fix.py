def populate_neighbors(self, data):
    data = data['TABLE_nbor']['ROW_nbor']
    if isinstance(data, dict):
        data = [data]
    objects = dict()
    for item in data:
        local_intf = item['l_port_id']
        if (local_intf not in objects):
            objects[local_intf] = list()
        nbor = dict()
        nbor['port'] = item['port_id']
        nbor['host'] = item['chassis_id']
        objects[local_intf].append(nbor)
    return objects