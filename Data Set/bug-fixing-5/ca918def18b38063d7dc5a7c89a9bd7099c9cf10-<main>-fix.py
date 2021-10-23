def main():
    argument_spec = openstack_full_argument_spec(zone=dict(required=True), name=dict(required=True), recordset_type=dict(required=False), records=dict(required=False, type='list'), description=dict(required=False, default=None), ttl=dict(required=False, default=None, type='int'), state=dict(default='present', choices=['absent', 'present']))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, required_if=[('state', 'present', ['recordset_type', 'records'])], supports_check_mode=True, **module_kwargs)
    zone = module.params.get('zone')
    name = module.params.get('name')
    state = module.params.get('state')
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        recordset_type = module.params.get('recordset_type')
        recordset_filter = {
            'type': recordset_type,
        }
        recordsets = cloud.search_recordsets(zone, name_or_id=name, filters=recordset_filter)
        if (len(recordsets) == 1):
            recordset = recordsets[0]
            try:
                recordset_id = recordset['id']
            except KeyError as e:
                module.fail_json(msg=str(e))
        else:
            recordset = None
        if (state == 'present'):
            records = module.params.get('records')
            description = module.params.get('description')
            ttl = module.params.get('ttl')
            if module.check_mode:
                module.exit_json(changed=_system_state_change(state, records, description, ttl, zone, recordset))
            if (recordset is None):
                recordset = cloud.create_recordset(zone=zone, name=name, recordset_type=recordset_type, records=records, description=description, ttl=ttl)
                changed = True
            else:
                if (records is None):
                    records = []
                pre_update_recordset = recordset
                changed = _system_state_change(state, records, description, ttl, zone, pre_update_recordset)
                if changed:
                    zone = cloud.update_recordset(zone, recordset_id, records=records, description=description, ttl=ttl)
            module.exit_json(changed=changed, recordset=recordset)
        elif (state == 'absent'):
            if module.check_mode:
                module.exit_json(changed=_system_state_change(state, None, None, None, None, recordset))
            if (recordset is None):
                changed = False
            else:
                cloud.delete_recordset(zone, recordset_id)
                changed = True
            module.exit_json(changed=changed)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))