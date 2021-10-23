

def main():
    argument_spec = openstack_full_argument_spec(state=dict(required=False, default='present', choices=['absent', 'present']), name=dict(required=False), ram=dict(required=False, type='int'), vcpus=dict(required=False, type='int'), disk=dict(required=False, type='int'), ephemeral=dict(required=False, default=0, type='int'), swap=dict(required=False, default=0, type='int'), rxtx_factor=dict(required=False, default=1.0, type='float'), is_public=dict(required=False, default=True, type='bool'), flavorid=dict(required=False, default='auto'), extra_specs=dict(required=False, default=None, type='dict'))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, supports_check_mode=True, required_if=[('state', 'present', ['ram', 'vcpus', 'disk'])], **module_kwargs)
    state = module.params['state']
    name = module.params['name']
    extra_specs = (module.params['extra_specs'] or {
        
    })
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        flavor = cloud.get_flavor(name)
        if module.check_mode:
            module.exit_json(changed=_system_state_change(module, flavor))
        if (state == 'present'):
            if (not flavor):
                flavor = cloud.create_flavor(name=name, ram=module.params['ram'], vcpus=module.params['vcpus'], disk=module.params['disk'], flavorid=module.params['flavorid'], ephemeral=module.params['ephemeral'], swap=module.params['swap'], rxtx_factor=module.params['rxtx_factor'], is_public=module.params['is_public'])
                changed = True
            else:
                changed = False
            old_extra_specs = flavor['extra_specs']
            new_extra_specs = dict([(k, str(v)) for (k, v) in extra_specs.items()])
            unset_keys = (set(flavor['extra_specs'].keys()) - set(extra_specs.keys()))
            if unset_keys:
                cloud.unset_flavor_specs(flavor['id'], unset_keys)
            if (old_extra_specs != new_extra_specs):
                cloud.set_flavor_specs(flavor['id'], extra_specs)
            changed = (changed or (old_extra_specs != new_extra_specs))
            module.exit_json(changed=changed, flavor=flavor, id=flavor['id'])
        elif (state == 'absent'):
            if flavor:
                cloud.delete_flavor(name)
                module.exit_json(changed=True)
            module.exit_json(changed=False)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))
