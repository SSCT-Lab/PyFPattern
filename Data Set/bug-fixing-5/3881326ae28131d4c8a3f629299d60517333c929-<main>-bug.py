def main():
    argument_spec = purefa_argument_spec()
    argument_spec.update(dict(gather_subset=dict(default='minimum', type='list')))
    module = AnsibleModule(argument_spec, supports_check_mode=False)
    array = get_system(module)
    subset = [test.lower() for test in module.params['gather_subset']]
    valid_subsets = ('all', 'minimum', 'config', 'performance', 'capacity', 'network', 'subnet', 'interfaces', 'hgroups', 'pgroups', 'hosts', 'admins', 'volumes', 'snapshots', 'pods', 'vgroups', 'offload', 'apps', 'arrays')
    subset_test = ((test in valid_subsets) for test in subset)
    if (not all(subset_test)):
        module.fail_json(msg=('value must gather_subset must be one or more of: %s, got: %s' % (','.join(valid_subsets), ','.join(subset))))
    info = {
        
    }
    if (('minimum' in subset) or ('all' in subset)):
        info['default'] = generate_default_dict(array)
    if (('performance' in subset) or ('all' in subset)):
        info['performance'] = generate_perf_dict(array)
    if (('config' in subset) or ('all' in subset)):
        info['config'] = generate_config_dict(array)
    if (('capacity' in subset) or ('all' in subset)):
        info['capacity'] = generate_capacity_dict(array)
    if (('network' in subset) or ('all' in subset)):
        info['network'] = generate_network_dict(array)
    if (('subnet' in subset) or ('all' in subset)):
        info['subnet'] = generate_subnet_dict(array)
    if (('interfaces' in subset) or ('all' in subset)):
        info['interfaces'] = generate_interfaces_dict(array)
    if (('hosts' in subset) or ('all' in subset)):
        info['hosts'] = generate_host_dict(array)
    if (('volumes' in subset) or ('all' in subset)):
        info['volumes'] = generate_vol_dict(array)
    if (('snapshots' in subset) or ('all' in subset)):
        info['snapshots'] = generate_snap_dict(array)
    if (('hgroups' in subset) or ('all' in subset)):
        info['hgroups'] = generate_hgroups_dict(array)
    if (('pgroups' in subset) or ('all' in subset)):
        info['pgroups'] = generate_pgroups_dict(array)
    if (('pods' in subset) or ('all' in subset)):
        info['pods'] = generate_pods_dict(array)
    if (('admins' in subset) or ('all' in subset)):
        info['admins'] = generate_admin_dict(array)
    if (('vgroups' in subset) or ('all' in subset)):
        info['vgroups'] = generate_vgroups_dict(array)
    if (('offload' in subset) or ('all' in subset)):
        info['nfs_offload'] = generate_nfs_offload_dict(array)
        info['s3_offload'] = generate_s3_offload_dict(array)
    if (('apps' in subset) or ('all' in subset)):
        info['apps'] = generate_apps_dict(array)
    if (('arrays' in subset) or ('all' in subset)):
        info['arrays'] = generate_conn_array_dict(array)
    module.exit_json(changed=False, purefa_info=info)