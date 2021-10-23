def populate_structured_neighbors_lldp(self, data):
    objects = dict()
    data = data['TABLE_nbor']['ROW_nbor']
    if isinstance(data, dict):
        data = [data]
    for item in data:
        local_intf = normalize_interface(item['l_port_id'])
        objects[local_intf] = list()
        nbor = dict()
        nbor['port'] = item['port_id']
        nbor['host'] = nbor['sysname'] = item['chassis_id']
        objects[local_intf].append(nbor)
    return objects