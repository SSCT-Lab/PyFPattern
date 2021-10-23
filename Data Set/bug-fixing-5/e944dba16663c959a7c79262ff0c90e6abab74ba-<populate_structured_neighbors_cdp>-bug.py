def populate_structured_neighbors_cdp(self, data):
    objects = dict()
    data = data['TABLE_cdp_neighbor_detail_info']['ROW_cdp_neighbor_detail_info']
    if isinstance(data, dict):
        data = [data]
    for item in data:
        local_intf = item['intf_id']
        objects[local_intf] = list()
        nbor = dict()
        nbor['port'] = item['port_id']
        nbor['sysname'] = item['device_id']
        objects[local_intf].append(nbor)
    return objects