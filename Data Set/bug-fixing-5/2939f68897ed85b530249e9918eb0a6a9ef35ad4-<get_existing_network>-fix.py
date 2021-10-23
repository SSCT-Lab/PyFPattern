def get_existing_network(self):
    try:
        return self.client.inspect_network(self.parameters.network_name)
    except NotFound:
        return None