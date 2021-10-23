def get_volumes():
    out = run_gluster(['volume', 'info'])
    volumes = {
        
    }
    volume = {
        
    }
    for row in out.split('\n'):
        if (': ' in row):
            (key, value) = row.split(': ')
            if (key.lower() == 'volume name'):
                volume['name'] = value
                volume['options'] = {
                    
                }
                volume['quota'] = False
            if (key.lower() == 'volume id'):
                volume['id'] = value
            if (key.lower() == 'status'):
                volume['status'] = value
            if (key.lower() == 'transport-type'):
                volume['transport'] = value
            if value.lower().endswith(' (arbiter)'):
                if ('arbiters' not in volume):
                    volume['arbiters'] = []
                value = value[:(- 10)]
                volume['arbiters'].append(value)
            elif (key.lower() == 'number of bricks'):
                volume['replicas'] = value[(- 1):]
            if ((key.lower() != 'bricks') and (key.lower()[:5] == 'brick')):
                if ('bricks' not in volume):
                    volume['bricks'] = []
                volume['bricks'].append(value)
            if ('.' in key):
                if ('options' not in volume):
                    volume['options'] = {
                        
                    }
                volume['options'][key] = value
                if ((key == 'features.quota') and (value == 'on')):
                    volume['quota'] = True
        elif ((row.lower() != 'bricks:') and (row.lower() != 'options reconfigured:')):
            if (len(volume) > 0):
                volumes[volume['name']] = volume
            volume = {
                
            }
    return volumes