def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(name=dict(), display_name=dict(), group=dict(), state=dict(choices=['present', 'deployed', 'started', 'stopped', 'restarted', 'restored', 'absent', 'destroyed', 'expunged'], default='present'), service_offering=dict(), cpu=dict(type='int'), cpu_speed=dict(type='int'), memory=dict(type='int'), template=dict(), iso=dict(), template_filter=dict(default='executable', aliases=['iso_filter'], choices=['all', 'featured', 'self', 'selfexecutable', 'sharedexecutable', 'executable', 'community']), networks=dict(type='list', aliases=['network']), ip_to_networks=dict(type='list', aliases=['ip_to_network']), ip_address=dict(), ip6_address=dict(), disk_offering=dict(), disk_size=dict(type='int'), root_disk_size=dict(type='int'), keyboard=dict(type='str', choices=['de', 'de-ch', 'es', 'fi', 'fr', 'fr-be', 'fr-ch', 'is', 'it', 'jp', 'nl-be', 'no', 'pt', 'uk', 'us']), hypervisor=dict(choices=CS_HYPERVISORS), host=dict(), security_groups=dict(type='list', aliases=['security_group']), affinity_groups=dict(type='list', aliases=['affinity_group']), domain=dict(), account=dict(), project=dict(), user_data=dict(), zone=dict(), ssh_key=dict(), force=dict(type='bool', default=False), tags=dict(type='list', aliases=['tag']), details=dict(type='dict'), poll_async=dict(type='bool', default=True), allow_root_disk_shrink=dict(type='bool', default=False)))
    required_together = cs_required_together()
    required_together.extend([['cpu', 'cpu_speed', 'memory']])
    module = AnsibleModule(argument_spec=argument_spec, required_together=required_together, required_one_of=(['display_name', 'name'],), mutually_exclusive=(['template', 'iso'],), supports_check_mode=True)
    acs_instance = AnsibleCloudStackInstance(module)
    state = module.params.get('state')
    if (state in ['absent', 'destroyed']):
        instance = acs_instance.absent_instance()
    elif (state in ['expunged']):
        instance = acs_instance.expunge_instance()
    elif (state in ['restored']):
        acs_instance.present_instance()
        instance = acs_instance.restore_instance()
    elif (state in ['present', 'deployed']):
        instance = acs_instance.present_instance()
    elif (state in ['stopped']):
        acs_instance.present_instance(start_vm=False)
        instance = acs_instance.stop_instance()
    elif (state in ['started']):
        acs_instance.present_instance()
        instance = acs_instance.start_instance()
    elif (state in ['restarted']):
        acs_instance.present_instance()
        instance = acs_instance.restart_instance()
    if (instance and ('state' in instance) and (instance['state'].lower() == 'error')):
        module.fail_json(msg=("Instance named '%s' in error state." % module.params.get('name')))
    result = acs_instance.get_result(instance)
    module.exit_json(**result)