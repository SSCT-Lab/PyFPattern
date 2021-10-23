def _format_items(self, items, project_disks):
    '\n            :param items: A list of hosts\n        '
    for host in items:
        if ('zone' in host):
            host['zone_selflink'] = host['zone']
            host['zone'] = host['zone'].split('/')[(- 1)]
        if ('machineType' in host):
            host['machineType_selflink'] = host['machineType']
            host['machineType'] = host['machineType'].split('/')[(- 1)]
        if ('networkInterfaces' in host):
            for network in host['networkInterfaces']:
                if ('network' in network):
                    network['network'] = self._format_network_info(network['network'])
                if ('subnetwork' in network):
                    network['subnetwork'] = self._format_network_info(network['subnetwork'])
        host['project'] = host['selfLink'].split('/')[6]
        host['image'] = self._get_image(host, project_disks)
    return items