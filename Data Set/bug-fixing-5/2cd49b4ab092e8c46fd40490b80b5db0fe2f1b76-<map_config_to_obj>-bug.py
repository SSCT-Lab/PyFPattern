def map_config_to_obj(module):
    objs = []
    try:
        out = run_commands(module, ['show ip route | json'])[0]
    except IndexError:
        out = {
            
        }
    if out:
        try:
            vrfs = out['vrfs']['default']['routes']
        except (AttributeError, KeyError, TypeError):
            vrfs = {
                
            }
    if vrfs:
        for address in vrfs:
            obj = {
                
            }
            obj['address'] = address
            obj['admin_distance'] = vrfs[address].get('preference')
            obj['next_hop'] = vrfs[address].get('vias')[0].get('nexthopAddr')
            objs.append(obj)
    return objs