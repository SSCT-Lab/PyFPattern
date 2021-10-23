def parse_power_supply_info(self, data):
    objects = list()
    for l in data.splitlines():
        if (l == ''):
            break
        if l[0].isdigit():
            obj = {
                
            }
            line = l.split()
            obj['model'] = line[1]
            obj['number'] = line[0]
            obj['status'] = line[(- 1)]
            objects.append(obj)
    return objects