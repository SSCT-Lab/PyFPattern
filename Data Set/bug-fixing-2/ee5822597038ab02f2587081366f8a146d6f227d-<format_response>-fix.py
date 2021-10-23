

def format_response(self, item):
    d = item.as_dict()
    iv = self.mgmt_client.virtual_machine_scale_set_vms.get_instance_view(resource_group_name=self.resource_group, vm_scale_set_name=self.vmss_name, instance_id=d.get('instance_id', None)).as_dict()
    power_state = ''
    for index in range(len(iv['statuses'])):
        code = iv['statuses'][index]['code'].split('/')
        if (code[0] == 'PowerState'):
            power_state = code[1]
            break
    d = {
        'resource_group': self.resource_group,
        'id': d.get('id', None),
        'tags': d.get('tags', None),
        'instance_id': d.get('instance_id', None),
        'latest_model': d.get('latest_model_applied', None),
        'name': d.get('name', None),
        'provisioning_state': d.get('provisioning_state', None),
        'power_state': power_state,
        'vm_id': d.get('vm_id', None),
        'image_reference': d.get('storage_profile').get('image_reference', None),
        'computer_name': d.get('os_profile').get('computer_name', None),
    }
    return d
