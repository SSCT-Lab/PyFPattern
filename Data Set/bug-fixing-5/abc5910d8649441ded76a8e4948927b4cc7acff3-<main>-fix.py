def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent'], default='present'), name=dict(default=None, required=True), ballooning=dict(default=None, type='bool', aliases=['balloon']), gluster=dict(default=None, type='bool'), virt=dict(default=None, type='bool'), threads_as_cores=dict(default=None, type='bool'), ksm_numa=dict(default=None, type='bool'), ksm=dict(default=None, type='bool'), ha_reservation=dict(default=None, type='bool'), trusted_service=dict(default=None, type='bool'), vm_reason=dict(default=None, type='bool'), host_reason=dict(default=None, type='bool'), memory_policy=dict(default=None, choices=['disabled', 'server', 'desktop']), rng_sources=dict(default=None, type='list'), spice_proxy=dict(default=None), fence_enabled=dict(default=None, type='bool'), fence_skip_if_sd_active=dict(default=None, type='bool'), fence_skip_if_connectivity_broken=dict(default=None, type='bool'), fence_connectivity_threshold=dict(default=None, type='int'), resilience_policy=dict(default=None, choices=['migrate_highly_available', 'migrate', 'do_not_migrate']), migration_bandwidth=dict(default=None, choices=['auto', 'hypervisor_default', 'custom']), migration_bandwidth_limit=dict(default=None, type='int'), migration_auto_converge=dict(default=None, choices=['true', 'false', 'inherit']), migration_compressed=dict(default=None, choices=['true', 'false', 'inherit']), migration_policy=dict(default=None, choices=['legacy', 'minimal_downtime', 'suspend_workload', 'post_copy']), serial_policy=dict(default=None, choices=['vm', 'host', 'custom']), serial_policy_value=dict(default=None), scheduling_policy=dict(default=None), data_center=dict(default=None), description=dict(default=None), comment=dict(default=None), network=dict(default=None), cpu_arch=dict(default=None, choices=['ppc64', 'undefined', 'x86_64']), cpu_type=dict(default=None), switch_type=dict(default=None, choices=['legacy', 'ovs']), compatibility_version=dict(default=None), mac_pool=dict(default=None))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (module._name == 'ovirt_clusters'):
        module.deprecate("The 'ovirt_clusters' module is being renamed 'ovirt_cluster'", version=2.8)
    check_sdk(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        clusters_service = connection.system_service().clusters_service()
        clusters_module = ClustersModule(connection=connection, module=module, service=clusters_service)
        state = module.params['state']
        if (state == 'present'):
            ret = clusters_module.create()
        elif (state == 'absent'):
            ret = clusters_module.remove()
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))