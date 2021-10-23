def populate_neighbors(self, data):
    data = data['TABLE_nbor']
    if isinstance(data, dict):
        data = [data]
    objects = dict()
    for item in data:
        local_intf = item['ROW_nbor']['l_port_id']
        if (local_intf not in objects):
            objects[local_intf] = list()
        nbor = dict()
        nbor['port'] = item['ROW_nbor']['port_id']
        nbor['host'] = item['ROW_nbor']['chassis_id']
        objects[local_intf].append(nbor)
    return objects