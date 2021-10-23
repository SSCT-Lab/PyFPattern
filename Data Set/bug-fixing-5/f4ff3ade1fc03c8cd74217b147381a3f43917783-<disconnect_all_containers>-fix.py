def disconnect_all_containers(self):
    containers = self.client.get_network(name=self.parameters.name)['Containers']
    if (not containers):
        return
    for cont in containers.values():
        self.disconnect_container(cont['Name'])