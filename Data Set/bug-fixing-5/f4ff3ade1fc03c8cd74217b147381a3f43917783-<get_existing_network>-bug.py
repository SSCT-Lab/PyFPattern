def get_existing_network(self):
    return self.client.get_network(name=self.parameters.network_name)