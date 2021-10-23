def main():
    argument_spec = ovirt_facts_full_argument_spec(name=dict(default=None), host=dict(default=None), vm=dict(default=None))
    module = AnsibleModule(argument_spec)
    if (module._name == 'ovirt_affinity_labels_facts'):
        module.deprecate("The 'ovirt_affinity_labels_facts' module is being renamed 'ovirt_affinity_label_facts'", version=2.8)
    check_sdk(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        affinity_labels_service = connection.system_service().affinity_labels_service()
        labels = []
        all_labels = affinity_labels_service.list()
        if module.params['name']:
            labels.extend([l for l in all_labels if fnmatch.fnmatch(l.name, module.params['name'])])
        if module.params['host']:
            hosts_service = connection.system_service().hosts_service()
            if (search_by_name(hosts_service, module.params['host']) is None):
                raise Exception(("Host '%s' was not found." % module.params['host']))
            labels.extend([label for label in all_labels for host in connection.follow_link(label.hosts) if fnmatch.fnmatch(hosts_service.service(host.id).get().name, module.params['host'])])
        if module.params['vm']:
            vms_service = connection.system_service().vms_service()
            if (search_by_name(vms_service, module.params['vm']) is None):
                raise Exception(("Vm '%s' was not found." % module.params['vm']))
            labels.extend([label for label in all_labels for vm in connection.follow_link(label.vms) if fnmatch.fnmatch(vms_service.service(vm.id).get().name, module.params['vm'])])
        if (not (module.params['vm'] or module.params['host'] or module.params['name'])):
            labels = all_labels
        module.exit_json(changed=False, ansible_facts=dict(ovirt_affinity_labels=[get_dict_of_struct(struct=l, connection=connection, fetch_nested=module.params.get('fetch_nested'), attributes=module.params.get('nested_attributes')) for l in labels]))
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))