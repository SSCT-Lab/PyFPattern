def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent', 'plugged', 'unplugged'], default='present'), vm=dict(required=True), name=dict(required=True), interface=dict(default=None), profile=dict(default=None), network=dict(default=None), mac_address=dict(default=None))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    check_sdk(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        vms_service = connection.system_service().vms_service()
        vm_name = module.params.get('vm')
        vm = search_by_name(vms_service, vm_name)
        if (vm is None):
            raise Exception(("VM '%s' was not found." % vm_name))
        vm_service = vms_service.vm_service(vm.id)
        nics_service = vm_service.nics_service()
        vmnics_module = VmNicsModule(connection=connection, module=module, service=nics_service)
        profile = module.params.get('profile')
        if (profile and module.params['network']):
            cluster_name = get_link_name(connection, vm.cluster)
            dcs_service = connection.system_service().data_centers_service()
            dc = dcs_service.list(search=('Clusters.name=%s' % cluster_name))[0]
            networks_service = dcs_service.service(dc.id).networks_service()
            network = next((n for n in networks_service.list() if (n.name == module.params['network'])), None)
            if (network is None):
                raise Exception(("Network '%s' was not found in datacenter '%s'." % (module.params['network'], dc.name)))
            for vnic in connection.system_service().vnic_profiles_service().list():
                if ((vnic.name == profile) and (vnic.network.id == network.id)):
                    vmnics_module.vnic_id = vnic.id
        state = module.params['state']
        if (state == 'present'):
            ret = vmnics_module.create()
        elif (state == 'absent'):
            ret = vmnics_module.remove()
        elif (state == 'plugged'):
            vmnics_module.create()
            ret = vmnics_module.action(action='activate', action_condition=(lambda nic: (not nic.plugged)), wait_condition=(lambda nic: nic.plugged))
        elif (state == 'unplugged'):
            vmnics_module.create()
            ret = vmnics_module.action(action='deactivate', action_condition=(lambda nic: nic.plugged), wait_condition=(lambda nic: (not nic.plugged)))
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))