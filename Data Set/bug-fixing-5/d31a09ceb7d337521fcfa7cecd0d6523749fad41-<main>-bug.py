def main():
    argument_spec = openstack_full_argument_spec(name=dict(required=True), state=dict(default='present', choices=['absent', 'present']), backup_gigabytes=dict(required=False, type='int', default=None), backups=dict(required=False, type='int', default=None), cores=dict(required=False, type='int', default=None), fixed_ips=dict(required=False, type='int', default=None), floating_ips=dict(required=False, type='int', default=None, aliases=['compute_floating_ips']), floatingip=dict(required=False, type='int', default=None, aliases=['network_floating_ips']), gigabytes=dict(required=False, type='int', default=None), gigabytes_types=dict(required=False, type='dict', default={
        
    }), injected_file_size=dict(required=False, type='int', default=None), injected_files=dict(required=False, type='int', default=None), injected_path_size=dict(required=False, type='int', default=None), instances=dict(required=False, type='int', default=None), key_pairs=dict(required=False, type='int', default=None), network=dict(required=False, type='int', default=None), per_volume_gigabytes=dict(required=False, type='int', default=None), port=dict(required=False, type='int', default=None), project=dict(required=False, type='int', default=None), properties=dict(required=False, type='int', default=None), ram=dict(required=False, type='int', default=None), rbac_policy=dict(required=False, type='int', default=None), router=dict(required=False, type='int', default=None), security_group_rule=dict(required=False, type='int', default=None), security_group=dict(required=False, type='int', default=None), server_group_members=dict(required=False, type='int', default=None), server_groups=dict(required=False, type='int', default=None), snapshots=dict(required=False, type='int', default=None), snapshots_types=dict(required=False, type='dict', default={
        
    }), subnet=dict(required=False, type='int', default=None), subnetpool=dict(required=False, type='int', default=None), volumes=dict(required=False, type='int', default=None), volumes_types=dict(required=False, type='dict', default={
        
    }))
    module = AnsibleModule(argument_spec, supports_check_mode=True)
    if (not HAS_SHADE):
        module.fail_json(msg='shade is required for this module')
    try:
        cloud_params = dict(module.params)
        cloud = shade.operator_cloud(**cloud_params)
        dynamic_types = ['gigabytes_types', 'snapshots_types', 'volumes_types']
        for dynamic_type in dynamic_types:
            for (k, v) in module.params[dynamic_type].items():
                module.params[k] = int(v)
        project_quota_output = _get_quotas(cloud, cloud_params['name'])
        changes_required = False
        if (module.params['state'] == 'absent'):
            if module.check_mode:
                module.exit_json(changed=True)
            neutron_msg1 = 'network client call failed: Quota for tenant'
            neutron_msg2 = 'could not be found'
            for quota_type in project_quota_output.keys():
                quota_call = getattr(cloud, ('delete_%s_quotas' % quota_type))
                try:
                    quota_call(cloud_params['name'])
                except shade.OpenStackCloudException as e:
                    error_msg = str(e)
                    if ((error_msg.find(neutron_msg1) > (- 1)) and (error_msg.find(neutron_msg2) > (- 1))):
                        pass
                    else:
                        module.fail_json(msg=str(e), extra_data=e.extra_data)
            project_quota_output = _get_quotas(cloud, cloud_params['name'])
            changes_required = True
        elif (module.params['state'] == 'present'):
            if module.check_mode:
                module.exit_json(changed=_system_state_change(module, project_quota_output))
            (changes_required, quota_change_request) = _system_state_change_details(module, project_quota_output)
            if changes_required:
                for quota_type in quota_change_request.keys():
                    quota_call = getattr(cloud, ('set_%s_quotas' % quota_type))
                    quota_call(cloud_params['name'], **quota_change_request[quota_type])
                project_quota_update = _get_quotas(cloud, cloud_params['name'])
                if (project_quota_output == project_quota_update):
                    module.fail_json(msg='Could not apply quota update')
                project_quota_output = project_quota_update
        module.exit_json(changed=changes_required, openstack_quotas=project_quota_output)
    except shade.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)