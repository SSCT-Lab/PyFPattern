def main():
    argument_spec = openstack_full_argument_spec(image=dict(required=False))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        if module.params['image']:
            image = cloud.get_image(module.params['image'])
            module.exit_json(changed=False, ansible_facts=dict(openstack_image=image))
        else:
            images = cloud.list_images()
            module.exit_json(changed=False, ansible_facts=dict(openstack_image=images))
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))