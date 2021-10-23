

def get_existing_network(self):
    networks = self.client.networks(names=[self.parameters.network_name])
    if (not networks):
        networks = self.client.networks(ids=[self.parameters.network_name])
    if (not networks):
        return None
    else:
        return networks[0]
