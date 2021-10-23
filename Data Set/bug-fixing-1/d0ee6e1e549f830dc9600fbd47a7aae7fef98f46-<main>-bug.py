

def main():
    argument_spec = openstack_full_argument_spec(name=dict(required=True), id=dict(default=None), checksum=dict(default=None), disk_format=dict(default='qcow2', choices=['ami', 'ari', 'aki', 'vhd', 'vmdk', 'raw', 'qcow2', 'vdi', 'iso', 'vhdx', 'ploop']), container_format=dict(default='bare', choices=['ami', 'aki', 'ari', 'bare', 'ovf', 'ova', 'docker']), owner=dict(default=None), min_disk=dict(type='int', default=0), min_ram=dict(type='int', default=0), is_public=dict(type='bool', default=False), filename=dict(default=None), ramdisk=dict(default=None), kernel=dict(default=None), properties=dict(type='dict', default={
        
    }), state=dict(default='present', choices=['absent', 'present']))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        changed = False
        if module.params['checksum']:
            image = cloud.get_image(name_or_id=None, filters={
                'checksum': module.params['checksum'],
            })
        else:
            image = cloud.get_image(name_or_id=module.params['name'])
        if (module.params['state'] == 'present'):
            if (not image):
                kwargs = {
                    
                }
                if (module.params['id'] is not None):
                    kwargs['id'] = module.params['id']
                image = cloud.create_image(name=module.params['name'], filename=module.params['filename'], disk_format=module.params['disk_format'], container_format=module.params['container_format'], wait=module.params['wait'], timeout=module.params['timeout'], is_public=module.params['is_public'], min_disk=module.params['min_disk'], min_ram=module.params['min_ram'], **kwargs)
                changed = True
                if (not module.params['wait']):
                    module.exit_json(changed=changed, image=image, id=image.id)
            cloud.update_image_properties(image=image, kernel=module.params['kernel'], ramdisk=module.params['ramdisk'], **module.params['properties'])
            image = cloud.get_image(name_or_id=image.id)
            module.exit_json(changed=changed, image=image, id=image.id)
        elif (module.params['state'] == 'absent'):
            if (not image):
                changed = False
            else:
                cloud.delete_image(name_or_id=module.params['name'], wait=module.params['wait'], timeout=module.params['timeout'])
                changed = True
            module.exit_json(changed=changed)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)
