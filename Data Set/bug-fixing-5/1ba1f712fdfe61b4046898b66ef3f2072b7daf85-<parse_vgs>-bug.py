def parse_vgs(data):
    vgs = []
    for line in data.splitlines():
        parts = line.strip().split(';')
        vgs.append({
            'name': parts[0],
            'size': locale.atof(parts[1]),
            'free': locale.atof(parts[2]),
            'ext_size': locale.atof(parts[3]),
        })
    return vgs