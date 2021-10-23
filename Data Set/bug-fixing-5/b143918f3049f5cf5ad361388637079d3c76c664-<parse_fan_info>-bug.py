def parse_fan_info(self, data):
    objects = list()
    for l in data.splitlines():
        if (('-----------------' in l) or ('Status' in l)):
            continue
        line = l.split()
        if (len(line) > 1):
            obj = {
                
            }
            obj['name'] = line[0]
            obj['model'] = line[1]
            obj['hw_ver'] = line[(- 2)]
            obj['status'] = line[(- 1)]
            objects.append(obj)
    return objects