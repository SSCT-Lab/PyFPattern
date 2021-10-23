def host_vmk_update(self):
    '\n        Update VMKernel with given parameters\n        Returns: NA\n\n        '
    changed = changed_settings = changed_vds = changed_services = changed_service_vmotion = changed_service_mgmt = changed_service_ft = changed_service_vsan = changed_service_prov = changed_service_rep = changed_service_rep_nfc = False
    changed_list = []
    results = dict(changed=False, msg='')
    results['tcpip_stack'] = self.tcpip_stack
    net_stack_instance_key = self.get_api_net_stack_instance(self.tcpip_stack)
    if (self.vnic.spec.netStackInstanceKey != net_stack_instance_key):
        self.module.fail_json(msg='The TCP/IP stack cannot be changed on an existing VMkernel adapter!')
    results['mtu'] = self.mtu
    if (self.vnic.spec.mtu != self.mtu):
        changed_settings = True
        changed_list.append('MTU')
        results['mtu_previous'] = self.vnic.spec.mtu
    results['ipv4'] = self.network_type
    results['ipv4_ip'] = self.ip_address
    results['ipv4_sm'] = self.subnet_mask
    if self.default_gateway:
        results['ipv4_gw'] = self.default_gateway
    else:
        results['ipv4_gw'] = 'No override'
    if self.vnic.spec.ip.dhcp:
        if (self.network_type == 'static'):
            changed_settings = True
            changed_list.append('IPv4 settings')
            results['ipv4_previous'] = 'DHCP'
    if (not self.vnic.spec.ip.dhcp):
        if (self.network_type == 'dhcp'):
            changed_settings = True
            changed_list.append('IPv4 settings')
            results['ipv4_previous'] = 'static'
        elif (self.network_type == 'static'):
            if (self.ip_address != self.vnic.spec.ip.ipAddress):
                changed_settings = True
                changed_list.append('IP')
                results['ipv4_ip_previous'] = self.vnic.spec.ip.ipAddress
            if (self.subnet_mask != self.vnic.spec.ip.subnetMask):
                changed_settings = True
                changed_list.append('SM')
                results['ipv4_sm_previous'] = self.vnic.spec.ip.subnetMask
            if self.default_gateway:
                try:
                    if (self.default_gateway != self.vnic.spec.ipRouteSpec.ipRouteConfig.defaultGateway):
                        changed_settings = True
                        changed_list.append('GW override')
                        results['ipv4_gw_previous'] = self.vnic.spec.ipRouteSpec.ipRouteConfig.defaultGateway
                except AttributeError:
                    changed_settings = True
                    changed_list.append('GW override')
                    results['ipv4_gw_previous'] = 'No override'
            else:
                try:
                    if self.vnic.spec.ipRouteSpec.ipRouteConfig.defaultGateway:
                        changed_settings = True
                        changed_list.append('GW override')
                        results['ipv4_gw_previous'] = self.vnic.spec.ipRouteSpec.ipRouteConfig.defaultGateway
                except AttributeError:
                    pass
    results['portgroup'] = self.port_group_name
    dvs_uuid = None
    if self.vswitch_name:
        results['switch'] = self.vswitch_name
        try:
            if self.vnic.spec.distributedVirtualPort.switchUuid:
                changed_vds = True
                changed_list.append('Virtual Port')
                dvs_uuid = self.vnic.spec.distributedVirtualPort.switchUuid
        except AttributeError:
            pass
        if changed_vds:
            results['switch_previous'] = self.find_dvs_by_uuid(dvs_uuid)
            self.dv_switch_obj = find_dvs_by_name(self.content, results['switch_previous'])
            results['portgroup_previous'] = self.find_dvspg_by_key(self.dv_switch_obj, self.vnic.spec.distributedVirtualPort.portgroupKey)
    elif self.vds_name:
        results['switch'] = self.vds_name
        try:
            if (self.vnic.spec.distributedVirtualPort.switchUuid != self.dv_switch_obj.uuid):
                changed_vds = True
                changed_list.append('Virtual Port')
                dvs_uuid = self.vnic.spec.distributedVirtualPort.switchUuid
        except AttributeError:
            changed_vds = True
            changed_list.append('Virtual Port')
        if changed_vds:
            results['switch_previous'] = self.find_dvs_by_uuid(dvs_uuid)
            results['portgroup_previous'] = self.vnic.spec.portgroup
            portgroups = self.get_all_port_groups_by_host(host_system=self.esxi_host_obj)
            for portgroup in portgroups:
                if (portgroup.spec.name == self.vnic.spec.portgroup):
                    results['switch_previous'] = portgroup.spec.vswitchName
    results['services'] = self.create_enabled_services_string()
    if (self.vnic.spec.netStackInstanceKey == 'defaultTcpipStack'):
        service_type_vmks = self.get_all_vmks_by_service_type()
        if ((self.enable_vmotion and (self.vnic.device not in service_type_vmks['vmotion'])) or ((not self.enable_vmotion) and (self.vnic.device in service_type_vmks['vmotion']))):
            changed_services = changed_service_vmotion = True
        if ((self.enable_mgmt and (self.vnic.device not in service_type_vmks['management'])) or ((not self.enable_mgmt) and (self.vnic.device in service_type_vmks['management']))):
            changed_services = changed_service_mgmt = True
        if ((self.enable_ft and (self.vnic.device not in service_type_vmks['faultToleranceLogging'])) or ((not self.enable_ft) and (self.vnic.device in service_type_vmks['faultToleranceLogging']))):
            changed_services = changed_service_ft = True
        if ((self.enable_vsan and (self.vnic.device not in service_type_vmks['vsan'])) or ((not self.enable_vsan) and (self.vnic.device in service_type_vmks['vsan']))):
            changed_services = changed_service_vsan = True
        if ((self.enable_provisioning and (self.vnic.device not in service_type_vmks['vSphereProvisioning'])) or ((not self.enable_provisioning) and (self.vnic.device in service_type_vmks['vSphereProvisioning']))):
            changed_services = changed_service_prov = True
        if ((self.enable_replication and (self.vnic.device not in service_type_vmks['vSphereReplication'])) or ((not self.enable_provisioning) and (self.vnic.device in service_type_vmks['vSphereReplication']))):
            changed_services = changed_service_rep = True
        if ((self.enable_replication_nfc and (self.vnic.device not in service_type_vmks['vSphereReplicationNFC'])) or ((not self.enable_provisioning) and (self.vnic.device in service_type_vmks['vSphereReplicationNFC']))):
            changed_services = changed_service_rep_nfc = True
        if changed_services:
            changed_list.append('services')
    if (changed_settings or changed_vds or changed_services):
        changed = True
        if self.module.check_mode:
            changed_suffix = ' would be updated'
        else:
            changed_suffix = ' updated'
        if (len(changed_list) > 2):
            message = ((', '.join(changed_list[:(- 1)]) + ', and ') + str(changed_list[(- 1)]))
        elif (len(changed_list) == 2):
            message = ' and '.join(changed_list)
        elif (len(changed_list) == 1):
            message = changed_list[0]
        message = (('VMkernel Adapter ' + message) + changed_suffix)
        if (changed_settings or changed_vds):
            vnic_config = vim.host.VirtualNic.Specification()
            ip_spec = vim.host.IpConfig()
            if (self.network_type == 'dhcp'):
                ip_spec.dhcp = True
            else:
                ip_spec.dhcp = False
                ip_spec.ipAddress = self.ip_address
                ip_spec.subnetMask = self.subnet_mask
                if self.default_gateway:
                    vnic_config.ipRouteSpec = vim.host.VirtualNic.IpRouteSpec()
                    vnic_config.ipRouteSpec.ipRouteConfig = vim.host.IpRouteConfig()
                    vnic_config.ipRouteSpec.ipRouteConfig.defaultGateway = self.default_gateway
                else:
                    vnic_config.ipRouteSpec = vim.host.VirtualNic.IpRouteSpec()
                    vnic_config.ipRouteSpec.ipRouteConfig = vim.host.IpRouteConfig()
            vnic_config.ip = ip_spec
            vnic_config.mtu = self.mtu
            if changed_vds:
                if self.vswitch_name:
                    vnic_config.portgroup = self.port_group_name
                elif self.vds_name:
                    vnic_config.distributedVirtualPort = vim.dvs.PortConnection()
                    vnic_config.distributedVirtualPort.switchUuid = self.dv_switch_obj.uuid
                    vnic_config.distributedVirtualPort.portgroupKey = self.port_group_obj.key
            try:
                if (not self.module.check_mode):
                    self.esxi_host_obj.configManager.networkSystem.UpdateVirtualNic(self.vnic.device, vnic_config)
            except vim.fault.NotFound as not_found:
                self.module.fail_json(msg=('Failed to update vmk as virtual network adapter cannot be found %s' % to_native(not_found.msg)))
            except vim.fault.HostConfigFault as host_config_fault:
                self.module.fail_json(msg=('Failed to update vmk due to host config issues : %s' % to_native(host_config_fault.msg)))
            except vim.fault.InvalidState as invalid_state:
                self.module.fail_json(msg=('Failed to update vmk as ipv6 address is specified in an ipv4 only system : %s' % to_native(invalid_state.msg)))
            except vmodl.fault.InvalidArgument as invalid_arg:
                self.module.fail_json(msg=('Failed to update vmk as IP address or Subnet Mask in the IP configurationare invalid or PortGroup does not exist : %s' % to_native(invalid_arg.msg)))
        if changed_services:
            changed_list.append('Services')
            services_previous = []
            vnic_manager = self.esxi_host_obj.configManager.virtualNicManager
            if changed_service_mgmt:
                if (self.vnic.device in service_type_vmks['management']):
                    services_previous.append('Mgmt')
                operation = ('select' if self.enable_mgmt else 'deselect')
                self.set_service_type(vnic_manager=vnic_manager, vmk=self.vnic, service_type='management', operation=operation)
            if changed_service_vmotion:
                if (self.vnic.device in service_type_vmks['vmotion']):
                    services_previous.append('vMotion')
                operation = ('select' if self.enable_vmotion else 'deselect')
                self.set_service_type(vnic_manager=vnic_manager, vmk=self.vnic, service_type='vmotion', operation=operation)
            if changed_service_ft:
                if (self.vnic.device in service_type_vmks['faultToleranceLogging']):
                    services_previous.append('FT')
                operation = ('select' if self.enable_ft else 'deselect')
                self.set_service_type(vnic_manager=vnic_manager, vmk=self.vnic, service_type='faultToleranceLogging', operation=operation)
            if changed_service_prov:
                if (self.vnic.device in service_type_vmks['vSphereProvisioning']):
                    services_previous.append('Prov')
                operation = ('select' if self.enable_provisioning else 'deselect')
                self.set_service_type(vnic_manager=vnic_manager, vmk=self.vnic, service_type='vSphereProvisioning', operation=operation)
            if changed_service_rep:
                if (self.vnic.device in service_type_vmks['vSphereReplication']):
                    services_previous.append('Repl')
                operation = ('select' if self.enable_replication else 'deselect')
                self.set_service_type(vnic_manager=vnic_manager, vmk=self.vnic, service_type='vSphereReplication', operation=operation)
            if changed_service_rep_nfc:
                if (self.vnic.device in service_type_vmks['vSphereReplicationNFC']):
                    services_previous.append('Repl_NFC')
                operation = ('select' if self.enable_replication_nfc else 'deselect')
                self.set_service_type(vnic_manager=vnic_manager, vmk=self.vnic, service_type='vSphereReplicationNFC', operation=operation)
            if changed_service_vsan:
                if (self.vnic.device in service_type_vmks['vsan']):
                    services_previous.append('VSAN')
                if self.enable_vsan:
                    results['vsan'] = self.set_vsan_service_type()
                else:
                    self.set_service_type(vnic_manager=vnic_manager, vmk=self.vnic, service_type='vsan', operation=operation)
            results['services_previous'] = ', '.join(services_previous)
    else:
        message = 'VMkernel Adapter already configured properly'
    results['changed'] = changed
    results['msg'] = message
    results['device'] = self.vnic.device
    self.module.exit_json(**results)