def do_zone_inventory(self, zone, token, tags):
    self.inventory.add_group(zone)
    zone_info = SCALEWAY_LOCATION[zone]
    url = _build_server_url(zone_info['api_endpoint'])
    all_servers = _fetch_information(url=url, token=token)
    for server_info in all_servers:
        groups = self.match_groups(server_info, tags)
        server_id = server_info['id']
        for group in groups:
            self.inventory.add_group(group=group)
            self.inventory.add_host(group=group, host=server_id)
            self._fill_host_variables(server_id=server_id, server_info=server_info)