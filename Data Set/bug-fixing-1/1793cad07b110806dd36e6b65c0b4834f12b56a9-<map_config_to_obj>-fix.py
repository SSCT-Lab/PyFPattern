

def map_config_to_obj(module):
    objs = []
    try:
        out = get_config(module, flags=['| include ip.route'])
    except IndexError:
        out = ''
    if out:
        lines = out.splitlines()
        for line in lines:
            obj = {
                
            }
            add_match = re.search('ip route ([\\d\\./]+)', line, re.M)
            if add_match:
                address = add_match.group(1)
                if is_address(address):
                    obj['address'] = address
                hop_match = re.search('ip route {0} ([\\d\\./]+)'.format(address), line, re.M)
                if hop_match:
                    hop = hop_match.group(1)
                    if is_hop(hop):
                        obj['next_hop'] = hop
                    dist_match = re.search('ip route {0} {1} (\\d+)'.format(address, hop), line, re.M)
                    if dist_match:
                        distance = dist_match.group(1)
                        obj['admin_distance'] = int(distance)
                    else:
                        obj['admin_distance'] = 1
            objs.append(obj)
    return objs
