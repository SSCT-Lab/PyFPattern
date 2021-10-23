

def get_existing_network(self):
    networks = self.client.networks()
    network = None
    for n in networks:
        if (n['Name'] == self.parameters.network_name):
            network = n
    return network
