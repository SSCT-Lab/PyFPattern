def parse_vgs(data):
    vgs = []
    for line in data.splitlines():
        parts = line.strip().split(';')
        vgs.append({
            'name': parts[0],
            'size': float(parts[1]),
            'free': float(parts[2]),
            'ext_size': float(parts[3]),
        })
    return vgs