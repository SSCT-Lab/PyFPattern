def _absent_volume(module, cloud):
    changed = False
    if cloud.volume_exists(module.params['display_name']):
        try:
            changed = cloud.delete_volume(name_or_id=module.params['display_name'], wait=module.params['wait'], timeout=module.params['timeout'])
        except shade.OpenStackCloudTimeout:
            module.exit_json(changed=changed)
    module.exit_json(changed=changed)