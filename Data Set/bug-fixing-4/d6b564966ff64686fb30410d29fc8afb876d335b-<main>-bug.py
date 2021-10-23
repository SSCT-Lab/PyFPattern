def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent'], default='present'), name=dict(default=None, aliases=['host'], required=True), bond=dict(default=None, type='dict'), interface=dict(default=None), networks=dict(default=None, type='list'), labels=dict(default=None, type='list'), check=dict(default=None, type='bool'), save=dict(default=None, type='bool'))
    module = AnsibleModule(argument_spec=argument_spec)
    check_sdk(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        hosts_service = connection.system_service().hosts_service()
        host_networks_module = HostNetworksModule(connection=connection, module=module, service=hosts_service)
        host = host_networks_module.search_entity()
        if (host is None):
            raise Exception(("Host '%s' was not found." % module.params['name']))
        bond = module.params['bond']
        interface = module.params['interface']
        networks = module.params['networks']
        labels = module.params['labels']
        nic_name = (bond.get('name') if bond else module.params['interface'])
        nics_service = hosts_service.host_service(host.id).nics_service()
        nic = search_by_name(nics_service, nic_name)
        state = module.params['state']
        if ((state == 'present') and ((nic is None) or host_networks_module.has_update(nics_service.service(nic.id)))):
            host_networks_module.action(entity=host, action='setup_networks', post_action=host_networks_module._action_save_configuration, check_connectivity=module.params['check'], modified_bonds=([otypes.HostNic(name=bond.get('name'), bonding=otypes.Bonding(options=[otypes.Option(name='mode', value=str(bond.get('mode')))], slaves=[otypes.HostNic(name=i) for i in bond.get('interfaces', [])]))] if bond else None), modified_labels=([otypes.NetworkLabel(name=str(name), host_nic=otypes.HostNic(name=(bond.get('name') if bond else interface))) for name in labels] if labels else None), modified_network_attachments=([otypes.NetworkAttachment(network=(otypes.Network(name=network['name']) if network['name'] else None), host_nic=otypes.HostNic(name=(bond.get('name') if bond else interface)), ip_address_assignments=[otypes.IpAddressAssignment(assignment_method=otypes.BootProtocol(network.get('boot_protocol', 'none')), ip=otypes.Ip(address=network.get('address'), gateway=network.get('gateway'), netmask=network.get('netmask'), version=(otypes.IpVersion(network.get('version')) if network.get('version') else None)))]) for network in networks] if networks else None))
        elif ((state == 'absent') and nic):
            attachments_service = nics_service.nic_service(nic.id).network_attachments_service()
            attachments = attachments_service.list()
            if networks:
                network_names = [network['name'] for network in networks]
                attachments = [attachment for attachment in attachments if (get_link_name(connection, attachment.network) in network_names)]
            if (labels or bond or attachments):
                host_networks_module.action(entity=host, action='setup_networks', post_action=host_networks_module._action_save_configuration, check_connectivity=module.params['check'], removed_bonds=([otypes.HostNic(name=bond.get('name'))] if bond else None), removed_labels=([otypes.NetworkLabel(name=str(name)) for name in labels] if labels else None), removed_network_attachments=list(attachments))
        nic = search_by_name(nics_service, nic_name)
        module.exit_json(**{
            'changed': host_networks_module.changed,
            'id': (nic.id if nic else None),
            'host_nic': get_dict_of_struct(nic),
        })
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))