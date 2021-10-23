def _present_volume(module, cloud):
    if cloud.volume_exists(module.params['display_name']):
        v = cloud.get_volume(module.params['display_name'])
        if (not _needs_update(module, v)):
            module.exit_json(changed=False, id=v['id'], volume=v)
        _modify_volume(module, cloud)
    diff = {
        'before': '',
        'after': '',
    }
    volume_args = dict(size=module.params['size'], volume_type=module.params['volume_type'], display_name=module.params['display_name'], display_description=module.params['display_description'], snapshot_id=module.params['snapshot_id'], bootable=module.params['bootable'], availability_zone=module.params['availability_zone'])
    if module.params['image']:
        image_id = cloud.get_image_id(module.params['image'])
        volume_args['imageRef'] = image_id
    if module.params['volume']:
        volume_id = cloud.get_volume_id(module.params['volume'])
        if (not volume_id):
            module.fail_json(msg=("Failed to find volume '%s'" % module.params['volume']))
        volume_args['source_volid'] = volume_id
    if module.params['scheduler_hints']:
        volume_args['scheduler_hints'] = module.params['scheduler_hints']
    if module.params['metadata']:
        volume_args['metadata'] = module.params['metadata']
    if module.check_mode:
        diff['after'] = volume_args
        module.exit_json(changed=True, id=None, volume=volume_args, diff=diff)
    volume = cloud.create_volume(wait=module.params['wait'], timeout=module.params['timeout'], **volume_args)
    diff['after'] = volume
    module.exit_json(changed=True, id=volume['id'], volume=volume, diff=diff)