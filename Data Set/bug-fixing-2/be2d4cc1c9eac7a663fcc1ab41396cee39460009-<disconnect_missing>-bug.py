

def disconnect_missing(self):
    containers = self.existing_network['Containers']
    if (not containers):
        return
    for c in containers.values():
        name = c['Name']
        if (name not in self.parameters.connected):
            self.disconnect_container(name)
