def _on_nic_response(self, nic_model, is_primary=False):
    if (nic_model.get('type') == 'Microsoft.Network/networkInterfaces'):
        nic = AzureNic(nic_model=nic_model, inventory_client=self._inventory_client, is_primary=is_primary)
        self.nics.append(nic)