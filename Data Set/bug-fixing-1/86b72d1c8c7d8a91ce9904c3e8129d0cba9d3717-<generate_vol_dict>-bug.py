

def generate_vol_dict(array):
    volume_facts = {
        
    }
    vols = array.list_volumes()
    for vol in range(0, len(vols)):
        volume = vols[vol]['name']
        volume_facts[volume] = {
            'size': vols[vol]['size'],
            'serial': vols[vol]['serial'],
            'hosts': [],
        }
    cvols = array.list_volumes(connect=True)
    for cvol in range(0, len(cvols)):
        volume = cvols[cvol]['name']
        voldict = [cvols[cvol]['host'], cvols[cvol]['lun']]
        volume_facts[volume]['hosts'].append(voldict)
    return volume_facts
