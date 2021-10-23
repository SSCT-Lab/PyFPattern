def main():
    argument_spec = openstack_full_argument_spec(name=dict(required=True), zone_type=dict(required=False, choice=['primary', 'secondary']), email=dict(required=False, default=None), description=dict(required=False, default=None), ttl=dict(required=False, default=None, type='int'), masters=dict(required=False, default=None, type='list'), state=dict(default='present', choices=['absent', 'present']))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, supports_check_mode=True, **module_kwargs)
    name = module.params.get('name')
    state = module.params.get('state')
    wait = module.params.get('wait')
    timeout = module.params.get('timeout')
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        zone = cloud.get_zone(name)
        if (state == 'present'):
            zone_type = module.params.get('zone_type')
            email = module.params.get('email')
            description = module.params.get('description')
            ttl = module.params.get('ttl')
            masters = module.params.get('masters')
            if module.check_mode:
                module.exit_json(changed=_system_state_change(state, email, description, ttl, masters, zone))
            if (zone is None):
                zone = cloud.create_zone(name=name, zone_type=zone_type, email=email, description=description, ttl=ttl, masters=masters)
                changed = True
            else:
                if (masters is None):
                    masters = []
                pre_update_zone = zone
                changed = _system_state_change(state, email, description, ttl, masters, pre_update_zone)
                if changed:
                    zone = cloud.update_zone(name, email=email, description=description, ttl=ttl, masters=masters)
            if wait:
                _wait(timeout, cloud, zone, state, module, sdk)
            module.exit_json(changed=changed, zone=zone)
        elif (state == 'absent'):
            if module.check_mode:
                module.exit_json(changed=_system_state_change(state, None, None, None, None, zone))
            if (zone is None):
                changed = False
            else:
                cloud.delete_zone(name)
                changed = True
            if wait:
                _wait(timeout, cloud, zone, state, module, sdk)
            module.exit_json(changed=changed)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))