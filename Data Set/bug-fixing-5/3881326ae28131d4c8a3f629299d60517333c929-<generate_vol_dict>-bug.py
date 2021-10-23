def generate_vol_dict(array):
    volume_info = {
        
    }
    vols = array.list_volumes()
    for vol in range(0, len(vols)):
        volume = vols[vol]['name']
        volume_info[volume] = {
            'source': vols[vol]['source'],
            'size': vols[vol]['size'],
            'serial': vols[vol]['serial'],
            'hosts': [],
            'bandwidth': '',
        }
    api_version = array._list_available_rest_versions()
    if (AC_REQUIRED_API_VERSION in api_version):
        qvols = array.list_volumes(qos=True)
        for qvol in range(0, len(qvols)):
            volume = qvols[qvol]['name']
            qos = qvols[qvol]['bandwidth_limit']
            volume_info[volume]['bandwidth'] = qos
        vvols = array.list_volumes(protocol_endpoint=True)
        for vvol in range(0, len(vvols)):
            volume = vvols[vvol]['name']
            volume_info[volume] = {
                'source': vvols[vvol]['source'],
                'serial': vvols[vvol]['serial'],
                'hosts': [],
            }
    cvols = array.list_volumes(connect=True)
    for cvol in range(0, len(cvols)):
        volume = cvols[cvol]['name']
        voldict = [cvols[cvol]['host'], cvols[cvol]['lun']]
        volume_info[volume]['hosts'].append(voldict)
    return volume_info