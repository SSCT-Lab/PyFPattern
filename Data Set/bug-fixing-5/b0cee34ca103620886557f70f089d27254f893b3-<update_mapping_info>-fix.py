def update_mapping_info(self):
    'Collect the current state of the storage array.'
    response = None
    try:
        (rc, response) = request((self.url + ('storage-systems/%s/graph' % self.ssid)), method='GET', headers=HEADERS, **self.creds)
    except Exception as error:
        self.module.fail_json(msg=('Failed to retrieve storage array graph. Id [%s]. Error [%s]' % (self.ssid, to_native(error))))
    target_reference = {
        
    }
    target_name = {
        
    }
    target_type = {
        
    }
    if ((self.target_type is None) or (self.target_type == 'host')):
        for host in response['storagePoolBundle']['host']:
            target_reference.update({
                host['hostRef']: host['name'],
            })
            target_name.update({
                host['name']: host['hostRef'],
            })
            target_type.update({
                host['name']: 'host',
            })
    if ((self.target_type is None) or (self.target_type == 'group')):
        for cluster in response['storagePoolBundle']['cluster']:
            if (self.target and (self.target_type is None) and (cluster['name'] == self.target) and (self.target in target_name.keys())):
                self.module.fail_json(msg=('Ambiguous target type: target name is used for both host and group targets! Id [%s]' % self.ssid))
            target_reference.update({
                cluster['clusterRef']: cluster['name'],
            })
            target_name.update({
                cluster['name']: cluster['clusterRef'],
            })
            target_type.update({
                cluster['name']: 'group',
            })
    volume_reference = {
        
    }
    volume_name = {
        
    }
    lun_name = {
        
    }
    for volume in response['volume']:
        volume_reference.update({
            volume['volumeRef']: volume['name'],
        })
        volume_name.update({
            volume['name']: volume['volumeRef'],
        })
        if volume['listOfMappings']:
            lun_name.update({
                volume['name']: volume['listOfMappings'][0]['lun'],
            })
    self.mapping_info = dict(lun_mapping=[dict(volume_reference=mapping['volumeRef'], map_reference=mapping['mapRef'], lun_mapping_reference=mapping['lunMappingRef'], lun=mapping['lun']) for mapping in response['storagePoolBundle']['lunMapping']], volume_by_reference=volume_reference, volume_by_name=volume_name, lun_by_name=lun_name, target_by_reference=target_reference, target_by_name=target_name, target_type_by_name=target_type)