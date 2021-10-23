def do_zone_inventory(self, zone, token, tags, hostname_preferences):
    self.inventory.add_group(zone)
    zone_info = SCALEWAY_LOCATION[zone]
    url = _build_server_url(zone_info['api_endpoint'])
    raw_zone_hosts_infos = _fetch_information(url=url, token=token)
    for host_infos in raw_zone_hosts_infos:
        hostname = self._filter_host(host_infos=host_infos, hostname_preferences=hostname_preferences)
        if (not hostname):
            continue
        groups = self.match_groups(host_infos, tags)
        for group in groups:
            self.inventory.add_group(group=group)
            self.inventory.add_host(group=group, host=hostname)
            self._fill_host_variables(host=hostname, server_info=host_infos)