def container_names_in_network(network):
    return [c['Name'] for c in network['Containers'].values()]