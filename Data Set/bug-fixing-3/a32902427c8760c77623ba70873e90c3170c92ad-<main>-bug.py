def main():
    'Module entrypoint.'
    module = initialise_module()
    if (not HAS_LINODE_DEPENDENCY):
        msg = 'The linode_v4 module requires the linode_api4 package'
        raise module.fail_json(msg=msg)
    client = build_client(module)
    instance = maybe_instance_from_label(module, client)
    if ((module.params['state'] == 'present') and (instance is not None)):
        module.exit_json(changed=False, instance=instance._raw_json)
    elif ((module.params['state'] == 'present') and (instance is None)):
        instance_json = create_linode(module, client, authorized_keys=module.params['authorized_keys'], group=module.params['group'], image=module.params['image'], label=module.params['label'], region=module.params['region'], root_pass=module.params['root_pass'], tags=module.params['tags'], ltype=module.params['type'])
        module.exit_json(changed=True, instance=instance_json)
    elif ((module.params['state'] == 'absent') and (instance is not None)):
        instance.delete()
        module.exit_json(changed=True, instance=instance._raw_json)
    elif ((module.params['state'] == 'absent') and (instance is None)):
        module.exit_json(changed=False, instance={
            
        })