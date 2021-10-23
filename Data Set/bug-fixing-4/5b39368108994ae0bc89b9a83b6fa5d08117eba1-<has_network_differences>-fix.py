def has_network_differences(self):
    '\n        Check if the container is connected to requested networks with expected options: links, aliases, ipv4, ipv6\n        '
    different = False
    differences = []
    if (not self.parameters.networks):
        return (different, differences)
    if (not self.container.get('NetworkSettings')):
        self.fail('has_missing_networks: Error parsing container properties. NetworkSettings missing.')
    connected_networks = self.container['NetworkSettings']['Networks']
    for network in self.parameters.networks:
        if (connected_networks.get(network['name'], None) is None):
            different = True
            differences.append(dict(parameter=network, container=None))
        else:
            diff = False
            if (network.get('ipv4_address') and (network['ipv4_address'] != connected_networks[network['name']].get('IPAddress'))):
                diff = True
            if (network.get('ipv6_address') and (network['ipv6_address'] != connected_networks[network['name']].get('GlobalIPv6Address'))):
                diff = True
            if (network.get('aliases') and (not connected_networks[network['name']].get('Aliases'))):
                diff = True
            if (network.get('aliases') and connected_networks[network['name']].get('Aliases')):
                for alias in network.get('aliases'):
                    if (alias not in connected_networks[network['name']].get('Aliases', [])):
                        diff = True
            if (network.get('links') and (not connected_networks[network['name']].get('Links'))):
                diff = True
            if (network.get('links') and connected_networks[network['name']].get('Links')):
                expected_links = []
                for (link, alias) in network['links']:
                    expected_links.append(('%s:%s' % (link, alias)))
                for link in expected_links:
                    if (link not in connected_networks[network['name']].get('Links', [])):
                        diff = True
            if diff:
                different = True
                differences.append(dict(parameter=network, container=dict(name=network['name'], ipv4_address=connected_networks[network['name']].get('IPAddress'), ipv6_address=connected_networks[network['name']].get('GlobalIPv6Address'), aliases=connected_networks[network['name']].get('Aliases'), links=connected_networks[network['name']].get('Links'))))
    return (different, differences)