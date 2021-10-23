

def main():
    argument_spec = purefb_argument_spec()
    argument_spec.update(dict(name=dict(required=True), eradicate=dict(default='false', type='bool'), nfs=dict(default='true', type='bool'), nfs_rules=dict(default='*(rw,no_root_squash)'), smb=dict(default='false', type='bool'), http=dict(default='false', type='bool'), snapshot=dict(default='false', type='bool'), fastremove=dict(default='false', type='bool'), hard_limit=dict(default='false', type='bool'), state=dict(default='present', choices=['present', 'absent']), size=dict()))
    module = AnsibleModule(argument_spec, supports_check_mode=True)
    if (not HAS_PURITY_FB):
        module.fail_json(msg='purity_fb sdk is required for this module')
    state = module.params['state']
    blade = get_blade(module)
    fs = get_fs(module, blade)
    if ((state == 'present') and (not fs)):
        create_fs(module, blade)
    elif ((state == 'present') and fs):
        modify_fs(module, blade)
    elif ((state == 'absent') and fs and (not fs.destroyed)):
        delete_fs(module, blade)
    elif ((state == 'absent') and fs and fs.destroyed and module.params['eradicate']):
        eradicate_fs(module, blade)
    elif ((state == 'absent') and (not fs)):
        module.exit_json(changed=False)
