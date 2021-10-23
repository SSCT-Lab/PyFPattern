

def disconnect_missing(self):
    if (not self.existing_network):
        return
    containers = self.existing_network['Containers']
    if (not containers):
        return
    for c in containers.values():
        name = c['Name']
        if (name not in self.parameters.connected):
            self.disconnect_container(name)
