def disconnect_missing(self):
    for c in self.existing_network['Containers'].values():
        name = c['Name']
        if (name not in self.parameters.connected):
            self.disconnect_container(name)