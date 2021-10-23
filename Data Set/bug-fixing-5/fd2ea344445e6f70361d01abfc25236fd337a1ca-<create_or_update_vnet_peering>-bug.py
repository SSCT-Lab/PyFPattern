def create_or_update_vnet_peering(self):
    '\n        Creates or Update Azure Virtual Network Peering.\n\n        :return: deserialized Azure Virtual Network Peering instance state dictionary\n        '
    self.log('Creating or Updating the Azure Virtual Network Peering {0}'.format(self.name))
    vnet_id = format_resource_id(self.virtual_network['name'], self.subscription_id, 'Microsoft.Network', 'virtualNetworks', self.virtual_network['resource_group'])
    remote_vnet_id = format_resource_id(self.remote_virtual_network['name'], self.subscription_id, 'Microsoft.Network', 'virtualNetworks', self.remote_virtual_network['resource_group'])
    peering = self.network_models.VirtualNetworkPeering(id=vnet_id, name=self.name, remote_virtual_network=self.network_models.SubResource(id=remote_vnet_id), allow_virtual_network_access=self.allow_virtual_network_access, allow_gateway_transit=self.allow_gateway_transit, allow_forwarded_traffic=self.allow_forwarded_traffic, use_remote_gateways=self.use_remote_gateways)
    try:
        response = self.network_client.virtual_network_peerings.create_or_update(self.resource_group, self.virtual_network['name'], self.name, peering)
        if isinstance(response, LROPoller):
            response = self.get_poller_result(response)
        return vnetpeering_to_dict(response)
    except CloudError as exc:
        self.fail('Error creating Azure Virtual Network Peering: {0}.'.format(exc.message))