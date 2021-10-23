

def main():
    argument_spec = purefa_argument_spec()
    argument_spec.update(dict(name=dict(type='str', required=True), suffix=dict(type='str'), restore=dict(type='str'), overwrite=dict(type='bool', default=False), target=dict(type='str'), eradicate=dict(type='bool', default=False), state=dict(type='str', default='present', choices=['absent', 'present', 'copy'])))
    required_if = [('state', 'copy', ['suffix', 'restore'])]
    module = AnsibleModule(argument_spec, required_if=required_if, supports_check_mode=False)
    if (module.params['suffix'] is None):
        suffix = ('snap-' + str((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0, 0)).total_seconds()))
        module.params['suffix'] = suffix.replace('.', '')
    if ((not module.params['target']) and module.params['restore']):
        module.params['target'] = module.params['restore']
    state = module.params['state']
    array = get_system(module)
    pgroup = get_pgroup(module, array)
    if (pgroup is None):
        module.fail_json(msg='Protection Group {0} does not exist'.format(module.params('pgroup')))
    pgsnap = get_pgsnapshot(module, array)
    if (pgsnap is None):
        module.fail_json(msg='Selected volume {0} does not exist in the Protection Group'.format(module.params('name')))
    if (':' in module.params['name']):
        rvolume = get_rpgsnapshot(module, array)
    else:
        rvolume = get_pgroupvolume(module, array)
    if ((state == 'copy') and rvolume):
        restore_pgsnapvolume(module, array)
    elif ((state == 'present') and pgroup and (not pgsnap)):
        create_pgsnapshot(module, array)
    elif ((state == 'present') and pgroup and pgsnap):
        update_pgsnapshot(module, array)
    elif ((state == 'present') and (not pgroup)):
        update_pgsnapshot(module, array)
    elif ((state == 'absent') and pgsnap):
        delete_pgsnapshot(module, array)
    elif ((state == 'absent') and (not pgsnap)):
        module.exit_json(changed=False)
