def disconnect_all_containers(self):
    containers = self.client.inspect_network(self.parameters.network_name)['Containers']
    for cont in containers.values():
        self.disconnect_container(cont['Name'])