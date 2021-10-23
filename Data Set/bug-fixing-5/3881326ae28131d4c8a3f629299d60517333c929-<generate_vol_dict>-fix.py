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
            if (P53_API_VERSION in api_version):
                iops = qvols[qvol]['iops_limit']
                volume_info[volume]['iops_limit'] = iops
        vvols = array.list_volumes(protocol_endpoint=True)
        for vvol in range(0, len(vvols)):
            volume = vvols[vvol]['name']
            volume_info[volume] = {
                'source': vvols[vvol]['source'],
                'serial': vvols[vvol]['serial'],
                'hosts': [],
            }
            if (P53_API_VERSION in array._list_available_rest_versions()):
                pe_e2ees = array.list_volumes(protocol_endpoint=True, host_encryption_key=True)
                for pe_e2ee in range(0, len(pe_e2ees)):
                    volume = pe_e2ees[pe_e2ee]['name']
                    volume_info[volume]['host_encryption_key_status'] = pe_e2ees[pe_e2ee]['host_encryption_key_status']
        if (P53_API_VERSION in array._list_available_rest_versions()):
            e2ees = array.list_volumes(host_encryption_key=True)
            for e2ee in range(0, len(e2ees)):
                volume = e2ees[e2ee]['name']
                volume_info[volume]['host_encryption_key_status'] = e2ees[e2ee]['host_encryption_key_status']
    cvols = array.list_volumes(connect=True)
    for cvol in range(0, len(cvols)):
        volume = cvols[cvol]['name']
        voldict = {
            'host': cvols[cvol]['host'],
            'lun': cvols[cvol]['lun'],
        }
        volume_info[volume]['hosts'].append(voldict)
    return volume_info