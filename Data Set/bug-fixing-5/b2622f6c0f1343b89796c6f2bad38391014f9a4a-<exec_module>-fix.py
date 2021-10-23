def exec_module(self, **kwargs):
    nsg = None
    subnet = None
    for key in self.module_arg_spec:
        setattr(self, key, kwargs[key])
    if (self.address_prefix_cidr and (not CIDR_PATTERN.match(self.address_prefix_cidr))):
        self.fail('Invalid address_prefix_cidr value {0}'.format(self.address_prefix_cidr))
    nsg = dict()
    if self.security_group:
        nsg = self.parse_nsg()
    route_table = dict()
    if self.route_table:
        route_table = self.parse_resource_to_dict(self.route_table)
        self.route_table = format_resource_id(val=route_table['name'], subscription_id=route_table['subscription_id'], namespace='Microsoft.Network', types='routeTables', resource_group=route_table['resource_group'])
    results = dict()
    changed = False
    try:
        self.log('Fetching subnet {0}'.format(self.name))
        subnet = self.network_client.subnets.get(self.resource_group, self.virtual_network_name, self.name)
        self.check_provisioning_state(subnet, self.state)
        results = subnet_to_dict(subnet)
        if (self.state == 'present'):
            if (self.address_prefix_cidr and (results['address_prefix'] != self.address_prefix_cidr)):
                self.log('CHANGED: subnet {0} address_prefix_cidr'.format(self.name))
                changed = True
                results['address_prefix'] = self.address_prefix_cidr
            if ((self.security_group is not None) and (results['network_security_group'].get('id') != nsg.get('id'))):
                self.log('CHANGED: subnet {0} network security group'.format(self.name))
                changed = True
                results['network_security_group']['id'] = nsg.get('id')
                results['network_security_group']['name'] = nsg.get('name')
            if ((self.route_table is not None) and (self.route_table != results['route_table'].get('id'))):
                changed = True
                results['route_table']['id'] = self.route_table
                self.log('CHANGED: subnet {0} route_table to {1}'.format(self.name, route_table.get('name')))
            if self.service_endpoints:
                oldd = {
                    
                }
                for item in self.service_endpoints:
                    name = item['service']
                    locations = (item.get('locations') or [])
                    oldd[name] = {
                        'service': name,
                        'locations': locations.sort(),
                    }
                newd = {
                    
                }
                if ('service_endpoints' in results):
                    for item in results['service_endpoints']:
                        name = item['service']
                        locations = (item.get('locations') or [])
                        newd[name] = {
                            'service': name,
                            'locations': locations.sort(),
                        }
                if (newd != oldd):
                    changed = True
                    results['service_endpoints'] = self.service_endpoints
        elif (self.state == 'absent'):
            changed = True
    except CloudError:
        if (self.state == 'present'):
            changed = True
    self.results['changed'] = changed
    self.results['state'] = results
    if (not self.check_mode):
        if ((self.state == 'present') and changed):
            if (not subnet):
                if (not self.address_prefix_cidr):
                    self.fail('address_prefix_cidr is not set')
                self.log('Creating subnet {0}'.format(self.name))
                subnet = self.network_models.Subnet(address_prefix=self.address_prefix_cidr)
                if nsg:
                    subnet.network_security_group = self.network_models.NetworkSecurityGroup(id=nsg.get('id'))
                if self.route_table:
                    subnet.route_table = self.network_models.RouteTable(id=self.route_table)
                if self.service_endpoints:
                    subnet.service_endpoints = self.service_endpoints
            else:
                self.log('Updating subnet {0}'.format(self.name))
                subnet = self.network_models.Subnet(address_prefix=results['address_prefix'])
                if (results['network_security_group'].get('id') is not None):
                    subnet.network_security_group = self.network_models.NetworkSecurityGroup(id=results['network_security_group'].get('id'))
                if (results['route_table'].get('id') is not None):
                    subnet.route_table = self.network_models.RouteTable(id=results['route_table'].get('id'))
                if (results.get('service_endpoints') is not None):
                    subnet.service_endpoints = results['service_endpoints']
            self.results['state'] = self.create_or_update_subnet(subnet)
        elif ((self.state == 'absent') and changed):
            self.delete_subnet()
            self.results['state']['status'] = 'Deleted'
    return self.results