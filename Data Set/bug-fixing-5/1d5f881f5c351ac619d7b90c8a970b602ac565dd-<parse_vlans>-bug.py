def parse_vlans(self, data):
    objects = list()
    data = data['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief']
    if isinstance(data, dict):
        objects.append(data['vlanshowbr-vlanid-utf'])
    elif isinstance(data, list):
        for item in data:
            objects.append(item['vlanshowbr-vlanid-utf'])
    return objects