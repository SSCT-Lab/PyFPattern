

def main():
    argument_spec = purefa_argument_spec()
    argument_spec.update(dict(name=dict(required=True), eradicate=dict(default='false', type='bool'), state=dict(default='present', choices=['present', 'absent']), size=dict()))
    required_if = [('state', 'present', ['size'])]
    module = AnsibleModule(argument_spec, required_if=required_if, supports_check_mode=True)
    if (not HAS_PURESTORAGE):
        module.fail_json(msg='purestorage sdk is required for this module in volume')
    state = module.params['state']
    array = get_system(module)
    volume = get_volume(module, array)
    if ((state == 'present') and (not volume)):
        create_volume(module, array)
    elif ((state == 'present') and volume):
        update_volume(module, array)
    elif ((state == 'absent') and volume):
        delete_volume(module, array)
    elif ((state == 'absent') and (not volume)):
        module.exit_json(changed=False)
