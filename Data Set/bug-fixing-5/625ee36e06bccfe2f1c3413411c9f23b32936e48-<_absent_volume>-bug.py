def _absent_volume(module, cloud):
    try:
        cloud.delete_volume(name_or_id=module.params['display_name'], wait=module.params['wait'], timeout=module.params['timeout'])
    except shade.OpenStackCloudTimeout:
        module.exit_json(changed=False)
    module.exit_json(changed=True)