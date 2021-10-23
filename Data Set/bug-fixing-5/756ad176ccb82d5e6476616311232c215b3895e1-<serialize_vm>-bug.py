def serialize_vm(self, vm):
    '\n        Convert a VirtualMachine object to dict.\n\n        :param vm: VirtualMachine object\n        :return: dict\n        '
    result = self.serialize_obj(vm, AZURE_OBJECT_CLASS, enum_modules=AZURE_ENUM_MODULES)
    resource_group = re.sub('\\/.*', '', re.sub('.*resourceGroups\\/', '', result['id']))
    instance = None
    power_state = None
    try:
        instance = self.compute_client.virtual_machines.instance_view(resource_group, vm.name)
        instance = self.serialize_obj(instance, AZURE_OBJECT_CLASS, enum_modules=AZURE_ENUM_MODULES)
    except Exception as exc:
        self.fail('Error getting virtual machine {0} instance view - {1}'.format(vm.name, str(exc)))
    for index in range(len(instance['statuses'])):
        code = instance['statuses'][index]['code'].split('/')
        if (code[0] == 'PowerState'):
            power_state = code[1]
        elif ((code[0] == 'OSState') and (code[1] == 'generalized')):
            power_state = 'generalized'
            break
    new_result = {
        
    }
    new_result['power_state'] = power_state
    new_result['id'] = vm.id
    new_result['resource_group'] = resource_group
    new_result['name'] = vm.name
    new_result['state'] = 'present'
    new_result['location'] = vm.location
    new_result['vm_size'] = result['properties']['hardwareProfile']['vmSize']
    new_result['admin_username'] = result['properties']['osProfile']['adminUsername']
    image = result['properties']['storageProfile'].get('imageReference')
    if (image is not None):
        if (image.get('publisher', None) is not None):
            new_result['image'] = {
                'publisher': image['publisher'],
                'sku': image['sku'],
                'offer': image['offer'],
                'version': image['version'],
            }
        else:
            new_result['image'] = {
                'id': image.get('id', None),
            }
    vhd = result['properties']['storageProfile']['osDisk'].get('vhd')
    if (vhd is not None):
        url = urlparse(vhd['uri'])
        new_result['storage_account_name'] = url.netloc.split('.')[0]
        new_result['storage_container_name'] = url.path.split('/')[1]
        new_result['storage_blob_name'] = url.path.split('/')[(- 1)]
    new_result['os_disk_caching'] = result['properties']['storageProfile']['osDisk']['caching']
    new_result['os_type'] = result['properties']['storageProfile']['osDisk']['osType']
    new_result['data_disks'] = []
    disks = result['properties']['storageProfile']['dataDisks']
    for disk_index in range(len(disks)):
        new_result['data_disks'].append({
            'lun': disks[disk_index]['lun'],
            'disk_size_gb': disks[disk_index]['diskSizeGB'],
            'managed_disk_type': disks[disk_index]['managedDisk']['storageAccountType'],
            'caching': disks[disk_index]['caching'],
        })
    new_result['network_interface_names'] = []
    nics = result['properties']['networkProfile']['networkInterfaces']
    for nic_index in range(len(nics)):
        new_result['network_interface_names'].append(re.sub('.*networkInterfaces/', '', nics[nic_index]['id']))
    new_result['tags'] = vm.tags
    return new_result